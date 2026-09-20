import subprocess, sys
from core2 import *
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
def run(ct,kn,maxd,step,ne,top=3):
    tk,al=KEYD[kn]
    out=subprocess.run(["./search3",ct,",".join(map(str,tk)),al,str(maxd),str(step),str(ne),str(top)],capture_output=True,text=True).stdout
    return [(float(l.split()[0]),l) for l in out.strip().split("\n") if l]
name=sys.argv[1]; keys=sys.argv[2].split(","); variants=sys.argv[3:] or [expand_dashes(MSGS[name])]
for v in variants:
    print("### variant len",len(v))
    for kn in keys:
        r=run(v,kn,6,1,2)+run(v,kn,4,2,3)
        r.sort(reverse=True)
        for sc,l in r[:3]: print(f"  {kn:10s} {l}")
        sys.stdout.flush()
