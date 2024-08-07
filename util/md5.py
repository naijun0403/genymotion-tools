import hashlib
import os

def calculate_md5(file: str) -> str:
    res = ''

    if os.path.isfile(file):
        with open(file, 'rb') as f:
            bytes = f.read()
            res = hashlib.md5(bytes).hexdigest()

    return res
