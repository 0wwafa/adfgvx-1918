import subprocess, sys
from core2 import *
from messages import MSGS
targets = sys.argv[1].split(",") if len(sys.argv)>1 else ["p73","p152","p153a","p153b","p158","p170","p176b","p189","p198","p217"]
maxd = sys.argv[2] if len(sys.argv)>2 else "5"
for name in targets:
    ct=expand_dashes(MSGS[name])
    allres=[]
    for kn,(tk,al) in KEYD.items():
        out=subprocess.run(["./search2",ct,",".join(map(str,tk)),al,maxd,"3","1"],capture_output=True,text=True).stdout
        for line in out.strip().split("\n"):
            if not line: continue
            sc=float(line.split()[0]); allres.append((sc,kn,line))
    allres.sort(reverse=True)
    print("=====",name,len(ct))
    for sc,kn,line in allres[:8]: print(f"  {kn:10s} {line}")
    sys.stdout.flush()
