import sys
from adfgvx import *
from messages import MSGS
targets = sys.argv[1:] or ["p73","p152","p153a","p153b","p158","p170","p176b","p189","p198","p217"]
for name in targets:
    ct = clean(MSGS[name]); n=len(ct)
    res=[]
    for kn,tk,al in KEYS:
        # baseline
        res.append((score(decrypt(ct,tk,al)),kn,"orig",0))
        # single deletions
        for i in range(n):
            c=ct[:i]+ct[i+1:]
            res.append((score(decrypt(c,tk,al)),kn,"del",i))
        # single insertions
        for i in range(n+1):
            for s in SYM:
                c=ct[:i]+s+ct[i:]
                res.append((score(decrypt(c,tk,al)),kn,"ins"+s,i))
        # insert 2 / delete 2 at same position (bigram-level errors)
        for i in range(n-1):
            c=ct[:i]+ct[i+2:]
            res.append((score(decrypt(c,tk,al)),kn,"del2",i))
    res.sort(reverse=True)
    print("=====",name,n)
    for r in res[:6]:
        sc,kn,op,i=r
        print(f"  {sc:.3f} {kn:10s} {op:5s} {i}")
    best=res[0]; kn=best[1]; tk,al=[(t,a) for k,t,a in KEYS if k==kn][0]
    # show best decrypt
    op,i=best[2],best[3]
    if op=="orig": c=ct
    elif op=="del": c=ct[:i]+ct[i+1:]
    elif op=="del2": c=ct[:i]+ct[i+2:]
    else: c=ct[:i]+op[3]+ct[i:]
    print("  ",decrypt(c,tk,al))
