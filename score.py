"""score.py — the shared score. Higher is better; a reading passes at score >= THRESHOLD."""
from lexicon import TAGS

THRESHOLD = 7      # calibrated on blocks 0-2000 with reader.py only: 1.70% pass there

def tags(w):
    return TAGS.get(w, set())

def is_conn(w):  return "C" in tags(w) and not (tags(w) & {"P", "N", "V", "J"})
def is_subj(w):  return bool(tags(w) & {"P", "N"})
def is_verb(w):  return "V" in tags(w)

def clauses(words):
    """Subject-verb pairs in a sensible order: S V, or S {aux/modifier} V, or S {is/was/were} complement."""
    out = []
    for i in range(len(words) - 1):
        if not is_subj(words[i]):
            continue
        a = words[i + 1]
        if is_verb(a) and (not is_subj(a) or "P" in tags(words[i]) or "J" in tags(a)):
            out.append((i, i + 1)); continue
        if i + 2 < len(words) and tags(a) & {"X", "M"}:
            b = words[i + 2]
            if is_verb(b) or ("X" in tags(a) and tags(b) & {"J", "N"}):
                out.append((i, i + 2))
    return out

def score(words):
    s = 0
    if len(set(words)) < len(words) - 1: s -= 2                   # repeats
    if is_conn(words[-1]) or words[-1] == "quiet": s -= 3          # ends on a connective
    s -= 2 * sum(1 for x, y in zip(words, words[1:]) if is_conn(x) and is_conn(y))   # two in a row
    cl = clauses(words)
    if not cl:
        return s - 5                                               # no subject + verb: cannot pass
    s += 2
    i, j = cl[0]
    if "P" in tags(words[i]) or j == i + 1: s += 1                 # tight clause
    if len([c for c in cl if c[0] > cl[0][1]]) >= 1: s += 1        # a second clause after the first
    if j + 1 < len(words) and tags(words[j + 1]) & {"N", "J"}: s += 1   # the verb has a complement
    nconn = sum(is_conn(w) for w in words)
    s += 1 if 1 <= nconn <= 3 else -1
    if is_subj(words[0]) and not is_conn(words[0]): s += 1        # the Sign is a thing
    return s
