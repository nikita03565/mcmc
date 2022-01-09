import copy
import json
import math
import multiprocessing
import os
import random
import re
from typing import List

import numpy as np

from utils import get_logger

logger = get_logger("decipherer")

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())

if config["language"] == "ru":
    ru = True
elif config["language"] == "en":
    ru = False
else:
    raise ValueError("Unknown language code in config")

log = config["log"]

if ru:
    file_name = "ru.txt"
else:
    file_name = "en.txt"

first_letter_idx_ru = ord("а")
last_letter_idx_ru = ord("я")

first_letter_idx_en = ord("a")
last_letter_idx_en = ord("z")

first_letter_idx = first_letter_idx_ru if ru else first_letter_idx_en
last_letter_idx = last_letter_idx_ru if ru else last_letter_idx_en

letters = list(chr(idx) for idx in range(first_letter_idx, last_letter_idx + 1))
if ru:
    letters.insert(6, "ё")

letters_dict = {letter: idx for idx, letter in enumerate(letters)}
letters_set = set(letters)
num_letters = len(letters)
max_threads = os.cpu_count()
data_dir = "data"


def get_letter_index(letter: str, letters_dict: dict, start: int = 1) -> int:
    """
    Small utility function to get `letter`'s index using `letters_dict` dictionary with offset by `start`
    """
    if letter == "":
        return 0
    return letters_dict[letter] + start


def clear_text(text: str, ru: bool = True) -> str:
    """
    Removes a-z characters (for russian language), repeated spaces and apostrophe
    """
    text_lower = text.lower()
    if ru:
        text_lower = re.sub(r"[a-z]", "", text_lower).replace("'", "")
    return re.sub(r"\s\s+", " ", text_lower)


def apply_mapping(string: str, mapping: list, letters_dict: dict) -> str:
    """
    Applies transformation to `string` using `mapping`
    """
    encoded = list(string.lower())
    for idx, char in enumerate(encoded):
        if char in mapping:
            encoded[idx] = mapping[get_letter_index(char, letters_dict, start=0)]
    return "".join(encoded)


def calc_prob(decoded_string: str, letters_dict: dict, probability_matrix: np.array) -> float:
    """
    Calculates log probability of characters following each other in string using probability matrix
    """
    log_prob = 0
    prev_letter = ""
    for cur_letter in decoded_string:
        if cur_letter in letters_set:
            prev_letter_idx = get_letter_index(prev_letter, letters_dict)
            cur_letter_idx = get_letter_index(cur_letter, letters_dict)
            log_prob += math.log(probability_matrix[prev_letter_idx, cur_letter_idx])
            prev_letter = cur_letter
        elif prev_letter != "":
            prev_letter_idx = get_letter_index(prev_letter, letters_dict)
            log_prob += math.log(probability_matrix[prev_letter_idx, 0])
            prev_letter = ""
    if prev_letter != "":
        prev_letter_idx = get_letter_index(prev_letter, letters_dict)
        log_prob += math.log(probability_matrix[prev_letter_idx, 0])
    return log_prob


def select_best_starts(text: str, alphabet: list, letters_dict: dict, probability_matrix: np.array) -> List[List[str]]:
    """
    Tries to find several best (max metric values) initial encoding mappings
    """
    max_attempts = 1000
    tries = []
    for _ in range(max_attempts):
        mapping = copy.copy(alphabet)
        random.shuffle(mapping)
        cur_decoded = apply_mapping(text, mapping, letters_dict)
        cur_loglike = calc_prob(cur_decoded, letters_dict, probability_matrix)
        tries.append((mapping, cur_loglike))

    tries_sorted = sorted(tries, key=lambda x: x[1], reverse=True)
    best_results = tries_sorted[:max_threads]

    for best in best_results:
        if log:
            logger.info(best[1])
    return [best[0] for best in best_results]


def process_one(args: tuple) -> str:
    """
    Main algorithm part.
    Basically we're trying to make one change to a mapping, apply it and decide if we should accept it.
    """
    if log:
        logger.info("started processing...")
    mapping, letters_dict, probability_matrix, ciphered_text = args

    i = 1
    max_iterations = 20000
    cur_decoded = apply_mapping(ciphered_text, mapping, letters_dict)
    cur_loglike = calc_prob(cur_decoded, letters_dict, probability_matrix)
    max_loglike = cur_loglike
    max_decoded = cur_decoded
    while i < max_iterations:
        sw1, sw2 = random.choices(range(0, num_letters), k=2)
        att_mapping = copy.copy(mapping)
        att_mapping[sw1], att_mapping[sw2] = att_mapping[sw2], att_mapping[sw1]
        att_decoded = apply_mapping(ciphered_text, att_mapping, letters_dict)
        att_loglike = calc_prob(att_decoded, letters_dict, probability_matrix)
        if random.uniform(0, 1) < math.exp(att_loglike - cur_loglike):
            mapping = att_mapping
            cur_decoded = att_decoded
            cur_loglike = att_loglike
            if cur_loglike > max_loglike:
                max_loglike = cur_loglike
                max_decoded = cur_decoded
            i += 1
    if log:
        logger.info(str(max_loglike) + " " + str(max_decoded))
    return max_decoded


def build_probability_matrix() -> np.ndarray:
    """
    Calculates matrix describing probabilities of letters following other letters in some text corpus.
    """
    with open(os.path.join(data_dir, file_name), "r", encoding="utf-8") as f:
        text = clear_text(f.read(), ru=ru)

    count_matrix = np.zeros((len(letters) + 1, len(letters) + 1))

    prev_letter = ""

    for cur_letter in text:
        prev_letter_idx = get_letter_index(prev_letter, letters_dict)
        if cur_letter in letters_set:
            cur_letter_idx = get_letter_index(cur_letter, letters_dict)
            count_matrix[prev_letter_idx, cur_letter_idx] += 1
            prev_letter = cur_letter
        elif prev_letter != "":
            count_matrix[prev_letter_idx, 0] += 1
            prev_letter = ""

    probability_matrix = count_matrix + 1
    probability_matrix = probability_matrix / probability_matrix.sum(axis=1)[:, None]
    return probability_matrix


def decipher_text(ciphered_text: str) -> List[str]:
    """
    Builds probability matrix, selects best starts and runs deciphering processes in parallel to get several possible
    results in the end.
    """
    if log:
        logger.info("Started deciphering")
    probability_matrix = build_probability_matrix()

    encoding_mapping = copy.copy(letters)
    random.shuffle(encoding_mapping)

    starts = select_best_starts(ciphered_text, letters, letters_dict, probability_matrix)

    letters_dict_arg = [letters_dict for _ in range(max_threads)]
    probability_matrix_arg = [probability_matrix for _ in range(max_threads)]
    ciphered_text_arg = [ciphered_text for _ in range(max_threads)]

    with multiprocessing.Pool(max_threads) as pool:
        results = pool.map(process_one, zip(starts, letters_dict_arg, probability_matrix_arg, ciphered_text_arg))
    return results
