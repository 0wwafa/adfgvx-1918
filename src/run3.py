import subprocess, sys
from core2 import *
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
targets=sys.argv[1].split(",")
for name in targets:
    ct=expand_dashes(MSGS[name])
    allres=[]
    for kn,(tk,al) in KEYD.items():
        out=subprocess.run(["./search3",ct,",".join(map(str,tk)),al,"5","5","3","2"],capture_output=True,text=True).stdout
        for line in out.strip().split("\n"):
            if line: allres.append((float(line.split()[0]),kn,line))
    allres.sort(reverse=True)
    print("=====",name,len(ct))
    for sc,kn,line in allres[:10]: print(f"  {kn:10s} {line}")
    sys.stdout.flush()
