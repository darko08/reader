#!/usr/bin/env python3
"""Bake alphabet.txt into reader.html and day.html.

Usage: python3 build.py            (expects alphabet.txt next to this file)

Refuses to build unless the file's SHA-256 matches the carved hash and the
anchor readings from the carving record come out exactly.
"""
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CARVED = "7483a0908ea1ae4553aa7808fceb6b414433064493bff353dca19ac73cb4b957"
ANCHORS = {
    "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f":
        (10, "diver welcomed skull vineyard where fishwife sang ancient"),
    "00000000000000000001bacec0b0fa9755c3ddc9de032d2deff0b08a29616488":
        (19, "tender sobbed one gate or narwhal meant gentle"),
    "000000000000000000012dd0da669d631c949621728a2feec24a039be0ebfc3b":
        (19, "i bore under cistern may peace murmured seaward"),
    "00000000000000000000f384479b64ec92657a8c461524f8eb00fe050078de73":
        (20, "cradle stirred drowned village could thunder came ancient"),
}


def read(cols, h):
    silence = len(h) - len(h.lstrip("0"))
    body = h[silence:silence + 16].ljust(16, "0")
    return silence, " ".join(cols[c][int(body[2 * c:2 * c + 2], 16) % 256] for c in range(8))


def main():
    raw = (HERE / "alphabet.txt").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != CARVED:
        sys.exit(f"alphabet.txt does not match the carving\n  got     {digest}\n  carved  {CARVED}")

    lines = raw.decode("utf-8").splitlines()
    if len(lines) != 8 * 257:
        sys.exit(f"expected 2,056 lines (8 x header + 256 words), got {len(lines)}")
    cols = [[w.strip() for w in lines[c * 257 + 1:(c + 1) * 257]] for c in range(8)]
    for c, col in enumerate(cols, 1):
        if col[0] != "quiet" or len(set(col)) != 256:
            sys.exit(f"column {c} is not 256 distinct words starting with 'quiet'")

    for h, want in ANCHORS.items():
        got = read(cols, h)
        if got != want:
            sys.exit(f"anchor reading failed for {h}\n  got   {got}\n  want  {want}")

    # glosses.txt: same layout as alphabet.txt, each line "word: gloss"
    gl = (HERE / "glosses.txt").read_text(encoding="utf-8").splitlines()
    if len(gl) != 8 * 257:
        sys.exit("glosses.txt must have 2,056 lines")
    glosses = []
    for c in range(8):
        col = []
        for i, line in enumerate(gl[c * 257 + 1:(c + 1) * 257]):
            w, g = line.split(": ", 1)
            if w != cols[c][i] or not g.strip():
                sys.exit(f"glosses.txt column {c + 1} index {i}: expected a gloss for {cols[c][i]!r}")
            col.append(g.strip())
        glosses.append(col)

    tpl = (HERE / "reader.template.html").read_text(encoding="utf-8")
    a, b = tpl.index("/*ALPHABET*/"), tpl.index("/*END*/") + len("/*END*/")
    page = tpl[:a] + json.dumps(cols, ensure_ascii=False, separators=(",", ":")) + tpl[b:]
    a, b = page.index("/*GLOSSES*/"), page.index("/*GEND*/") + len("/*GEND*/")
    page = page[:a] + json.dumps(glosses, ensure_ascii=False, separators=(",", ":")) + page[b:]
    (HERE / "reader.html").write_text(page, encoding="utf-8")

    # day.html: the same columns, plus the scorer's tags and sets for "the page's picks"
    sys.path.insert(0, str(HERE))
    import score8                      # merges lexicon.py tags with tags8.json into score.TAGS
    import score as base
    order = "PNVXMJC"
    tags = {w: "".join(l for l in order if l in t) for w, t in sorted(base.TAGS.items())}
    sets = json.loads((HERE / "sets8.json").read_text(encoding="utf-8"))
    day = (HERE / "day.template.html").read_text(encoding="utf-8")
    for start, end, value in (("/*ALPHABET*/", "/*END*/", cols), ("/*TAGS*/", "/*TEND*/", tags), ("/*SETS*/", "/*SEND*/", sets)):
        a, b = day.index(start), day.index(end) + len(end)
        day = day[:a] + json.dumps(value, ensure_ascii=False, separators=(",", ":")) + day[b:]
    (HERE / "day.html").write_text(day, encoding="utf-8")
    print("hash matches the carving, anchors read correctly, reader.html and day.html written")


if __name__ == "__main__":
    main()
