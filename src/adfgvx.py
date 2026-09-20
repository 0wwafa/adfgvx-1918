"""ADFGVX toolkit: keys, decryption, German scoring."""
import math, re, os, itertools

SYM = "ADFGVX"

# (name, transposition key (rank list), substitution alphabet 36 chars, '+' = unknown)
KEYS = [
 ("Sep19-21", [12,2,7,20,10,19,1,13,9,18,3,17,21,8,14,4,6,16,11,22,5,15], "D5613Q9KBNO0HY8EISJUTZFCW7VPML2ARG4X"),
 ("Oct4-6",   [4,13,3,14,1,16,9,15,5,19,10,18,6,17,7,20,11,21,8,12,22,2], "YN87PJ3WRUCIEO1SKLZX0DFBH6MT9A2QV54G"),
 ("Oct28-31", [6,15,12,16,5,7,14,4,13,8,11,1,17,2,10,3,18,9], "HI20SXRUWQY8EK7O619CBJAP453FDZTGLMVN"),
 ("Nov1-3",   [3,16,4,15,7,12,18,6,17,8,19,1,13,10,2,14,11,9,5], "UILOF9RCZVSX02G7QTD8WNB5JMHEKPY41A36"),
 ("Nov4-6",   [7,10,8,14,3,11,16,1,6,13,4,9,15,5,12,17,2], "17WHFLJ5D2UPEXKVZ9O0Q3Y6R8ABGITCMS4N"),
 ("Nov7-9",   [6,12,7,15,1,11,16,5,8,14,3,18,9,13,2,17,20,10,19,4], "PRMYUW3LZGES8C71QOV29ITB405KXH6AJNDF"),
 ("Nov10-12", [9,12,7,11,3,8,16,6,14,2,10,15,5,13,1,4], "4ARUT1OIFSKN35BZPVLD6JMXCWHQ2E7G08Y9"),
 ("Nov13-15a",[13,8,6,16,7,18,1,14,9,20,10,15,17,2,3,11,5,19,4,12], "JZLH+R++S+T+MKDWU+V+B+P++FAO+GIX+CNE"),
 ("Nov13-15b",[4,11,5,14,9,7,16,1,12,15,6,10,3,13,8,2], "H23BMUF15PX0DJLR4789S6VONKZQAWITEGCY"),
 ("Nov16-18", [7,12,1,14,8,16,13,9,19,3,15,4,10,18,6,2,11,17,5], "WG+EITNHUB2R++FDZJS+++PY+VQL+1OAXMKC"),
 ("Nov19-21", [13,20,3,16,7,14,4,12,8,11,5,15,2,18,17,10,19,6,1,9], "LC58QH7VI2YB9EURO60GX3MTFAKP1D4NJZSW"),
 ("Nov22-24", [6,12,16,7,14,22,11,18,1,15,8,10,20,2,13,21,3,17,19,5,9,4], "QNZ72XS4C0IJY3RBEKL9FD6GMTHUVWA5O8P1"),
 ("Nov25-28", [21,9,6,14,10,20,1,16,18,7,15,4,11,22,5,17,23,2,12,8,19,3,13], "HQ05DKZAOYM6BEIWTJ7PSCFLV94132NGURX8"),
 ("Nov28-Dec1",[9,3,14,10,2,8,15,4,16,11,5,13,6,12,1,7], "782GPY5OQHF91UDNI364TLVXEAR0JZBKMCSW"),
]

def clean(ct):
    return re.sub(r"[^ADFGVX]", "", ct.upper())

def untranspose(ct, key):
    """Inverse columnar transposition. key[i] = rank of column i (1-based)."""
    n = len(ct); k = len(key)
    rows, extra = divmod(n, k)
    lens = [rows + (1 if i < extra else 0) for i in range(k)]
    order = sorted(range(k), key=lambda i: key[i])
    cols = {}
    pos = 0
    for i in order:
        cols[i] = ct[pos:pos+lens[i]]; pos += lens[i]
    out = []
    for r in range(rows+1):
        for i in range(k):
            if r < lens[i]:
                out.append(cols[i][r])
    return "".join(out)

def transpose(pt_syms, key):
    k = len(key)
    order = sorted(range(k), key=lambda i: key[i])
    cols = ["" for _ in range(k)]
    for idx, c in enumerate(pt_syms):
        cols[idx % k] += c
    return "".join(cols[i] for i in order)

def unsubst(bigrams, alpha):
    out = []
    for i in range(0, len(bigrams)-1, 2):
        r = SYM.index(bigrams[i]); c = SYM.index(bigrams[i+1])
        out.append(alpha[r*6+c].lower())
    return "".join(out)

def decrypt(ct, key, alpha):
    ct = clean(ct)
    return unsubst(untranspose(ct, key), alpha)

def encrypt(pt, key, alpha):
    pt = pt.upper()
    s = ""
    for ch in pt:
        i = alpha.index(ch)
        s += SYM[i//6] + SYM[i%6]
    return transpose(s, key)

# ---------- German scoring (log quadgram-ish via built-in word/ngram list) ----------
_GERMAN = None
def german_model():
    global _GERMAN
    if _GERMAN is not None: return _GERMAN
    path = os.path.join(os.path.dirname(__file__), "..", "data", "military_vocab.txt")
    txt = open(path, encoding="utf-8").read().lower()
    txt = txt.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    txt = re.sub(r"[^a-z]", "", txt)
    from collections import Counter
    n = 4
    cnt = Counter(txt[i:i+n] for i in range(len(txt)-n+1))
    total = sum(cnt.values())
    floor = math.log10(0.01/total)
    model = {k: math.log10(v/total) for k, v in cnt.items()}
    _GERMAN = (model, floor)
    return _GERMAN

def score(pt):
    model, floor = german_model()
    s = re.sub(r"[^a-z]", "", pt)
    if len(s) < 4: return -999
    return sum(model.get(s[i:i+4], floor) for i in range(len(s)-3)) / (len(s)-3)
