"""score8.py — reader8 score = the shared structural score + a surprise bonus,
then a ranking pass that penalizes repeated endings.

Surprise (an unexpected word pair), max +4:
  +2  a non-human subject doing a human act        (tide remembered, stone prayed)
  +2  an abstract subject doing a physical act     (promise drowned, mercy rusted)
  +1  a physical verb taking an abstract object    (drank silence, buried name)
Ending penalty: after ranking, any final word that appears more than 3 times in the top 50
loses 2 points on its 4th and later appearances; repeat until no ending appears more than 3 times.
"""
import json, os
import score as base

_here = os.path.dirname(os.path.abspath(__file__))
_t = json.load(open(os.path.join(_here, "tags8.json")))
_s = json.load(open(os.path.join(_here, "sets8.json")))
TAGS = {w: set(t) for w, t in base.TAGS.items()}
for w, t in _t.items():
    TAGS.setdefault(w, set()).update(t)
base.TAGS = TAGS                     # the structural score reads reader8's tags
ABSTRACT, PEOPLE, HUMAN = set(_s["abstract"]), set(_s["people"]), set(_s["human_verbs"])

def surprise(words):
    b = 0
    for i, j in base.clauses(words):
        s, v = words[i], words[j]
        if s not in PEOPLE and s not in ABSTRACT and v in HUMAN: b += 2
        if s in ABSTRACT and base.is_verb(v) and v not in HUMAN: b += 2
    for k in range(len(words) - 1):
        v, o = words[k], words[k + 1]
        if base.is_verb(v) and v not in HUMAN and o in ABSTRACT: b += 1
    return min(b, 4)

def score(words):
    return base.score(words) + surprise(words)

def rank(rows, top=50, limit=3, penalty=2):
    """rows: dicts with 'words' (list) and 'height'. Returns rows sorted, with 'final' score."""
    for r in rows:
        r["final"] = score(r["words"])
    while True:
        rows.sort(key=lambda r: (-r["final"], r["height"]))
        seen, changed = {}, False
        for r in rows[:top]:
            end = r["words"][-1]
            seen[end] = seen.get(end, 0) + 1
            if seen[end] > limit:
                r["final"] -= penalty; changed = True
        if not changed:
            return rows
