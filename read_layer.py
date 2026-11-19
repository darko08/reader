#!/usr/bin/env python3
"""read_layer.py: read one block hash with the carved Alphabet. Needs only alphabet.txt.

Usage:
  python3 read_layer.py 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARVED = "7483a0908ea1ae4553aa7808fceb6b414433064493bff353dca19ac73cb4b957"


def load(path=os.path.join(HERE, "alphabet.txt")):
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest() != CARVED:
        sys.exit("alphabet.txt does not match the hash carved in block 976,509")
    cols = []
    for line in raw.decode("utf-8").split("\n"):
        if line.startswith("# column"):
            cols.append([])
        elif line:
            cols[-1].append(line)
    return cols


def read(block_hash, cols):
    h = block_hash.lower()
    silence = len(h) - len(h.lstrip("0"))
    body = h[silence:silence + 16]
    idx = [int(body[i:i + 2], 16) for i in range(0, 16, 2)]
    return silence, [cols[k][i] for k, i in enumerate(idx)]


if __name__ == "__main__":
    if len(sys.argv) != 2 or len(sys.argv[1]) != 64:
        sys.exit(__doc__)
    silence, words = read(sys.argv[1], load())
    print("silence", silence)
    print("reading", " ".join(words))
    print("sign   ", words[0])
