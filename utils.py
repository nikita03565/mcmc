import re

first_letter_idx = ord("а")
last_letter_idx = ord("я")


def get_letter_index(letter):
    if letter == "":
        return 0
    return ord(letter) - first_letter_idx + 1


def get_letter_from_index(index):
    return chr(first_letter_idx + index)


def clear_text(text):
    """removes a-z characters, repeated spaces and apostrophe"""
    text_with_removed_chars = re.sub(r"[a-z]", "", text.lower()).replace("'", "")
    return re.sub(r"\s\s+", " ", text_with_removed_chars)
