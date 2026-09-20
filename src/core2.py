import re, math
from adfgvx import KEYS, SYM, german_model

def clean_q(ct):
    """Keep unknown markers as '?'. Various dash chars = 1 unknown each; '(...)'/'{...}' groups kept."""
    ct = ct.upper()
    ct = re.sub(r"[()\{\}]", "", ct)
    out=[]
    for ch in ct:
        if ch in SYM: out.append(ch)
        elif ch in "-–—": out.append("?")
    return "".join(out)

def expand_dashes(raw):
    # in the transcript '—' sometimes stands for 3 dashes (auto-correct), '–' for 2. Handle group-wise: each group should be 5 long.
    groups = raw.upper().split()
    res=[]
    for g in groups:
        g = re.sub(r"[()\{\}]", "", g)
        known = sum(1 for c in g if c in SYM)
        if known>=5: res.append("".join(c for c in g if c in SYM)); continue
        # fill remaining with ?
        s="".join(c if c in SYM else "?" for c in g)
        # collapse: compute how many ? needed
        q = 5-known
        # rebuild by replacing dash runs proportionally: simple approach: place ? where dashes are, pad
        pieces = re.split(r"([-–—]+)", g)
        built=""
        dash_runs=[p for p in pieces if p and p[0] in "-–—"]
        if not dash_runs:
            built = "".join(c for c in g if c in SYM)
        else:
            # distribute q unknowns over dash runs, weighting by char count (— =3, – =2, - =1)
            w=[sum({'-':1,'–':2,'—':3}[c] for c in r) for r in dash_runs]
            tot=sum(w); alloc=[max(1,round(q*x/tot)) for x in w]
            # fix rounding
            while sum(alloc)>q:
                i=alloc.index(max(alloc)); alloc[i]-=1
            while sum(alloc)<q:
                i=alloc.index(min(alloc)); alloc[i]+=1
            ai=0
            for p in pieces:
                if not p: continue
                if p[0] in "-–—": built+="?"*alloc[ai]; ai+=1
                else: built+="".join(c for c in p if c in SYM)
        res.append(built)
    return "".join(res)

def untranspose(ct, key):
    n=len(ct); k=len(key)
    rows, extra = divmod(n,k)
    lens=[rows+(1 if i<extra else 0) for i in range(k)]
    order=sorted(range(k), key=lambda i:key[i])
    cols=[None]*k; pos=0
    for i in order:
        cols[i]=ct[pos:pos+lens[i]]; pos+=lens[i]
    out=[]
    for r in range(rows+1):
        for i in range(k):
            if r<lens[i]: out.append(cols[i][r])
    return "".join(out)

def unsubst(b, alpha):
    out=[]
    for i in range(0,len(b)-1,2):
        x,y=b[i],b[i+1]
        if x=="?" or y=="?": out.append("?"); continue
        ch=alpha[SYM.index(x)*6+SYM.index(y)]
        out.append(ch.lower() if ch!="+" else "?")
    return "".join(out)

def decrypt(ct,key,alpha): return unsubst(untranspose(ct,key),alpha)

_model=None
def score(pt):
    global _model
    if _model is None: _model=german_model()
    model,floor=_model
    s=pt; n=len(s)-3
    if n<1: return -999
    tot=0.0; cnt=0
    for i in range(n):
        q=s[i:i+4]
        if "?" in q: continue
        tot+=model.get(q,floor); cnt+=1
    if cnt==0: return -999
    return tot/cnt

def apply_edits(ct, edits):
    """edits: list of (pos, delta); delta>0 insert delta '?' at pos, delta<0 delete -delta chars at pos. Apply from right to left."""
    for pos,d in sorted(edits, reverse=True):
        if d>0: ct=ct[:pos]+"?"*d+ct[pos:]
        else: ct=ct[:pos]+ct[pos-d:]
    return ct

KEYD={n:(t,a) for n,t,a in KEYS}
