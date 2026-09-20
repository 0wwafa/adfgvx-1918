import subprocess, sys
from core2 import *
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
def sc1(ct,tk,al,maxd=3):
    out=subprocess.run(["./search2",ct,",".join(map(str,tk)),al,str(maxd),"1","0"],capture_output=True,text=True).stdout.strip()
    if not out: return (-99,"")
    p=out.split(); return (float(p[0]), out)
def rerank(t): 
    s=sorted(t); return [s.index(x)+1 for x in t]
def variants(tk):
    K=len(tk); vs={}
    # swap two positions in key (columns swapped in rectangle)
    for i in range(K):
        for j in range(i+1,K):
            t=list(tk); t[i],t[j]=t[j],t[i]; vs[f"swap{i},{j}"]=t
    # drop one element
    for i in range(K):
        t=tk[:i]+tk[i+1:]; vs[f"drop{i}"]=rerank(t)
    # insert an element with rank r at pos i
    for i in range(K+1):
        for r in range(1,K+2):
            t=[x+ (1 if x>=r else 0) for x in tk]; t=t[:i]+[r]+t[i:]; vs[f"ins{i}r{r}"]=t
    return vs
targets=sys.argv[1].split(","); keys=sys.argv[2].split(",") if len(sys.argv)>2 and sys.argv[2] else list(KEYD)
for name in targets:
    ct=expand_dashes(MSGS[name]); res=[]
    for kn in keys:
        tk,al=KEYD[kn]
        for vn,t in variants(tk).items():
            s,line=sc1(ct,t,al); res.append((s,f"{kn}/{vn}",line))
    res.sort(reverse=True)
    print("=====",name)
    for s,d,line in res[:6]: print(f"  {s:.4f} {d:22s} {line[:150]}")
    sys.stdout.flush()
