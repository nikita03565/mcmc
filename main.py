import os
import numpy as np
from utils import first_letter_idx, last_letter_idx, get_letter_index, get_letter_from_index, clear_text
data_dir = os.path.join("data")

with open(os.path.join(data_dir, "voyna-i-mir-tom-1-utf.txt"), "r", encoding="utf-8") as f:
    text = clear_text(f.read())


letters = list(chr(idx) for idx in range(first_letter_idx, last_letter_idx + 1))
letters_set = set(letters)
num_letters = len(letters)
# + 1 to track non letter characters, spaces or punctuation for example
mat = np.zeros((len(letters) + 1, len(letters) + 1))


prev_letter = ""

for cur_letter in text:
    prev_letter_idx = get_letter_index(prev_letter)
    if cur_letter in letters_set:
        cur_letter_idx = get_letter_index(cur_letter)
        mat[prev_letter_idx, cur_letter_idx] += 1
        prev_letter = cur_letter
    elif prev_letter != "":
        mat[prev_letter_idx, 0] += 1
        prev_letter = ""

print(mat)
new_mat = mat + 1
new_mat = new_mat/new_mat.sum(axis=1)[:, None]
print(new_mat)
