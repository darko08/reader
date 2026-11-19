#!/usr/bin/env python3
"""reader.py — read Bitcoin block hashes through the Alphabet.

Usage:
  python reader.py 0                 # one block
  python reader.py 689301
  python reader.py scan 0 1000       # scan a range, write hits.csv
"""
import sys, os, csv, time, json, urllib.request

API = "https://mempool.space/api"
CACHE = "hashes.txt"   # height<TAB>hash, so rescans after a word swap are instant

# --- Alphabet: 256 words. Index 0 must be 'quiet'. ---
# Indices 1-15 are connectives: the byte after the Silence always starts with a
# non-zero hex digit (>= 0x10), so these slots can never be the Sign.
CONNECTIVES_LOW = """
the a of and to in is was not it we you
who will were
""".split()
CONNECTIVES_REST = """
never always again under over through after before below between from with
no if but i us me what where when your then here
there
""".split()
CONTENT = """
salt tide deep cold drift drown sea wave current undertow brine flood
well rain ice mist foam silt reef shore harbor anchor rope net
keel hull sink float swim pressure breath hand eye mouth hunger bone
sleep wake blood heart skin tooth throat lung spine skull tongue ear
finger child mother father hollow beneath body face shoulder deeper weight pulse
lamp dark ember glass shadow burn fire smoke ash spark candle moon
star dawn dusk night morning lantern mirror gold one two three dead
nine ten now only last first none many half once answer call
name key word silence promise lie song prayer secret letter story question
echo voice cry oath debt law stone layer door wreck surface bottom
wall gate room sank heavy empty bridge tower stair cave mine shaft
chamber vault grave kept garden waiting asleep open close give take go
come wait remember forget fall rise dig carry keep lose find hold
hear see speak write break mend seal follow return leave stay hide
watch dream knock listen bury drink maker reader diver probe tender vow
mark sign chronicle static whisper imprint fear greed tenth drowned starved ghost
still away year hour day winter old new long slow home alone
together lost found held back chain down light iron mercy rust
""".split()
ALPHABET = ["quiet"] + CONNECTIVES_LOW + CONNECTIVES_REST + CONTENT
assert len(ALPHABET) == 256 and len(set(ALPHABET)) == 256

CONNECTIVES = set(CONNECTIVES_LOW + CONNECTIVES_REST)   # 40 of 256, about 15%

_cache = {}
if os.path.exists(CACHE):
    for line in open(CACHE):
        k, v = line.split()
        _cache[int(k)] = v

def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode()

def block_hash(height):
    if height in _cache:
        return _cache[height]
    h = get(f"{API}/block-height/{height}").strip()
    _cache[height] = h
    with open(CACHE, "a") as f:
        f.write(f"{height}\t{h}\n")
    return h

def read(h):
    silence = len(h) - len(h.lstrip("0"))
    body = h[silence:]
    idx = [int(body[i:i+2], 16) for i in range(0, 16, 2)]   # 8 bytes after the Silence
    words = [ALPHABET[i] for i in idx]
    return silence, idx, words

from score import score, THRESHOLD   # shared with reader8.py

def show(height):
    h = block_hash(height)
    silence, idx, words = read(h)
    print(f"block {height}")
    print(f"hash  {h}")
    print(f"silence {silence}  " + " ".join(["quiet"] * min(silence, 20)))
    print(f"words  {' '.join(words)}")
    print(f"sign   {words[0]}")
    print(f"idx    {idx}")
    print(f"score  {score(words)}  (pass >= {THRESHOLD})")

def scan(a, b, threshold=THRESHOLD, out="hits.csv"):
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["height","silence","score","sign","words","hash"])
        for height in range(a, b + 1):
            cached = height in _cache
            try:
                h = block_hash(height)
            except Exception as e:
                print("skip", height, e); time.sleep(1); continue
            silence, idx, words = read(h)
            sc = score(words)
            if sc >= threshold:
                w.writerow([height, silence, sc, words[0], " ".join(words), h]); f.flush()
                print(height, sc, " ".join(words))
            if not cached:
                time.sleep(0.15)   # be polite to the public API

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "scan":
        scan(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 2 and sys.argv[1] == "alphabet":
        open("alphabet.txt", "w").write("\n".join(ALPHABET) + "\n")
        print("wrote alphabet.txt")
    elif len(sys.argv) == 2:
        show(int(sys.argv[1]))
    else:
        print(__doc__)
