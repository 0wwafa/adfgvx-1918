import subprocess, sys
from core2 import *
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
def single(ct,tk,al,maxd,top):
    out=subprocess.run(["./search2",ct,",".join(map(str,tk)),al,str(maxd),str(top),"0"],capture_output=True,text=True).stdout
    res=[]
    for line in out.strip().split("\n"):
        if not line: continue
        p=line.split(); sc=float(p[0]); d=dict(x.split("=") for x in p[1:5])
        p1,d1=int(d["p1"]),int(d["d1"])
        res.append((sc,(p1,d1),p[5] if len(p)>5 else ""))
    return res
def beam(ct0,tk,al,maxd=6,width=60,depth=6):
    frontier=[(single(ct0,tk,al,maxd,1)[0][0],ct0,[])]
    best=frontier[0]
    for lvl in range(depth):
        cand={}
        for item in frontier:
            sc,ct,hist=item[0],item[1],item[2]
            for s2,ed,pt in single(ct,tk,al,maxd,width):
                c2=apply_edits(ct,[ed])
                if c2 not in cand or cand[c2][0]<s2: cand[c2]=(s2,c2,hist+[ed],pt)
        frontier=sorted(cand.values(),reverse=True)[:width]
        if frontier and frontier[0][0]>best[0]: best=frontier[0]
    return best
if __name__=="__main__":
    targets=sys.argv[1].split(","); keys=sys.argv[2].split(",") if len(sys.argv)>2 and sys.argv[2] else list(KEYD)
    for name in targets:
        ct0=expand_dashes(MSGS[name]); print("=====",name,len(ct0)); sys.stdout.flush()
        res=[]
        for kn in keys:
            tk,al=KEYD[kn]; b=beam(ct0,tk,al)
            print(f"  {kn:10s} {b[0]:.4f} {b[2]} {b[3] if len(b)>3 else ''}"); sys.stdout.flush()
