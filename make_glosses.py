#!/usr/bin/env python3
"""Build glosses.txt (same layout as alphabet.txt: 8 headers, 256 lines each, 'word: gloss')
from the per-role sources in gloss_src/. Fails if any of the 2,048 words has no gloss."""
import pathlib, sys
H = pathlib.Path(__file__).resolve().parent
def load(n):
    d = {}
    for l in (H / "gloss_src" / n).read_text().splitlines():
        if l.strip():
            w, g = l.split("=", 1); assert w not in d, (n, w); d[w] = g.strip()
    return d
nouns, verbs, c3, c5, c8 = (load(n) for n in ("nouns.txt", "verbs.txt", "col3.txt", "col5.txt", "col8.txt"))
lines = (H / "alphabet.txt").read_text().splitlines()
src = [nouns, verbs, None, nouns, c5, nouns, verbs, c8]
out, missing = [], []
for c in range(8):
    out.append(lines[c * 257])
    for i, w in enumerate(lines[c * 257 + 1:(c + 1) * 257]):
        if i == 0: g = "silence; nothing is said here"
        elif c == 2: g = c3.get(w) if i <= 30 else nouns.get(w)
        else: g = src[c].get(w)
        if not g: missing.append((c + 1, i, w)); g = "?"
        out.append(f"{w}: {g}")
if missing: sys.exit(f"missing glosses: {missing}")
(H / "glosses.txt").write_text("\n".join(out) + "\n")
print("glosses.txt written:", len(out), "lines")
