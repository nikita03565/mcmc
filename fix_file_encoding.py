import os

data_dir = "data"

with open(os.path.join(data_dir, "voyna-i-mir-tom-1.txt"), "r", encoding="WINDOWS-1251") as f:
    content = f.read()

print(content)
with open(os.path.join(data_dir, "voyna-i-mir-tom-1-utf.txt"), "w", encoding="utf-8") as f:
    f.write(content)
