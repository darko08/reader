#!/usr/bin/env python3
"""reader8.py — the positional Alphabet: each of the 8 readable bytes has its own 256-word column.

  1 subject   2 verb   3 object or connective   4 place
  5 connective or verb   6 subject   7 verb   8 final word

Index 0 of every column is 'quiet'. Every column holds 256 distinct words. Column 5 mixes connectives and plain verbs.
Column 1, indices 1-15, can never be read (the byte after the Silence is always >= 0x10);
they hold plain nouns, so pronouns can be the Sign.

Usage:
  python reader8.py 0
  python reader8.py scan 800000 802000      # writes hits8.csv
"""
import sys, csv
from reader import block_hash          # same fetch + hashes.txt cache
from score8 import score, rank
from score import THRESHOLD

from columns8 import COLUMNS   # eight columns, 256 distinct words each, index 0 = quiet

def read(h):
    silence = len(h) - len(h.lstrip("0"))
    body = h[silence:]
    idx = [int(body[i:i+2], 16) for i in range(0, 16, 2)]
    words = [COLUMNS[k][i] for k, i in enumerate(idx)]
    return silence, idx, words

def show(height):
    h = block_hash(height)
    silence, idx, words = read(h)
    print(f"block {height}\nhash  {h}")
    print(f"silence {silence}  " + " ".join(["quiet"] * min(silence, 20)))
    print(f"words  {' '.join(words)}\nsign   {words[0]}\nidx    {idx}")
    print(f"score  {score(words)}  (pass >= {THRESHOLD})")

def scan(a, b, out="hits8.csv"):
    rows = []
    for height in range(a, b + 1):
        h = block_hash(height)
        silence, idx, words = read(h)
        rows.append({"height": height, "silence": silence, "words": words, "hash": h})
    rank(rows)
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["rank","height","silence","score","sign","words","hash"])
        for n, r in enumerate(rows, 1):
            w.writerow([n, r["height"], r["silence"], r["final"], r["words"][0], " ".join(r["words"]), r["hash"]])

NAMES = ["subject", "verb", "object or connective", "place", "connective or verb", "subject", "verb", "final word"]

def write_alphabet(path="alphabet.txt"):
    """One header line per column, then its 256 words, one per line, in index order. UTF-8, LF line ends."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for k, (name, col) in enumerate(zip(NAMES, COLUMNS), 1):
            f.write(f"# column {k}: {name}\n")
            for w in col:
                f.write(w + "\n")
    print("wrote", path)

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "scan":
        scan(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 2 and sys.argv[1] == "alphabet":
        write_alphabet()
    elif len(sys.argv) == 2:
        show(int(sys.argv[1]))
    else:
        print(__doc__)
