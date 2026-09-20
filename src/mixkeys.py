import subprocess, sys, itertools
from core2 import *
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
def sc1(ct,tk,al,maxd=2):
    out=subprocess.run(["./search2",ct,",".join(map(str,tk)),al,str(maxd),"1","0"],capture_output=True,text=True).stdout.strip()
    if not out: return (-99,"")
    p=out.split(); return (float(p[0]), out)
targets=sys.argv[1].split(",")
names=list(KEYD)
for name in targets:
    ct=expand_dashes(MSGS[name]); res=[]
    for tn in names:
        tk=KEYD[tn][0]
        variants={"fwd":tk, "rev":[len(tk)+1-x for x in tk]}
        for vn,t in variants.items():
            for an in names:
                al=KEYD[an][1]
                s,line=sc1(ct,t,al); res.append((s,f"T={tn}/{vn} S={an}",line))
    # column-wise inscription variant = transposition applied to ct read in different way: emulate by decrypting with untranspose then treating as column-major
    res.sort(reverse=True)
    print("=====",name)
    for s,d,line in res[:6]: print(f"  {s:.4f} {d:28s} {line[:150]}")
    sys.stdout.flush()
