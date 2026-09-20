import subprocess, sys
from core2 import *
from messages import MSGS
def run(ct,tk,al,maxd,top,two=1):
    out=subprocess.run(["./search2",ct,",".join(map(str,tk)),al,str(maxd),str(top),str(two)],capture_output=True,text=True).stdout
    res=[]
    for line in out.strip().split("\n"):
        if not line: continue
        p=line.split()
        sc=float(p[0]); d=dict(x.split("=") for x in p[1:5]); pt=p[5] if len(p)>5 else ""
        p1,d1,p2,d2=int(d["p1"]),int(d["d1"]),int(d["p2"]),int(d["d2"])
        edits=[(p1,d1)]+([(p2,d2)] if p2>=0 else [])
        res.append((sc,edits,pt))
    return res
def apply(ct,edits):
    return apply_edits(ct,edits)
targets = sys.argv[1].split(",")
keys = sys.argv[2].split(",") if len(sys.argv)>2 and sys.argv[2] else list(KEYD)
maxd=int(sys.argv[3]) if len(sys.argv)>3 else 5
for name in targets:
    ct0=expand_dashes(MSGS[name])
    print("=====",name,len(ct0)); sys.stdout.flush()
    for kn in keys:
        tk,al=KEYD[kn]
        r1=run(ct0,tk,al,maxd,6)
        best=(r1[0][0],r1[0][1],r1[0][2],[])
        seen=set()
        for sc,ed,pt in r1[:4]:
            c1=apply(ct0,ed)
            if c1 in seen: continue
            seen.add(c1)
            r2=run(c1,tk,al,maxd,1)
            if r2 and r2[0][0]>best[0]: best=(r2[0][0],ed,r2[0][2],r2[0][1])
        print(f"  {kn:10s} {best[0]:.4f} {best[1]} + {best[3]}  {best[2]}"); sys.stdout.flush()
