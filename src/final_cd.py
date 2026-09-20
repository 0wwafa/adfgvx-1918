import subprocess,sys
from core2 import *
from messages import MSGS
plan={"p73":["Oct28-31","Nov7-9","Nov4-6"],"p152":["Nov7-9","Nov4-6"],"p158":["Nov7-9","Nov4-6"],"p170":["Nov10-12","Nov7-9"],
      "p176b":["Nov10-12","Nov13-15a","Nov13-15b"],"p189":["Nov13-15a","Nov13-15b","Nov10-12"],"p198":["Nov16-18","Nov13-15b","Nov13-15a","Nov19-21"],"p217":["Nov22-24","Nov19-21","Nov25-28"]}
for name in sys.argv[1].split(","):
    ct=expand_dashes(MSGS[name]); n=len(ct)
    for kn in plan[name]:
        tk,al=KEYD[kn]
        out=subprocess.run(["./coldesc",ct,",".join(map(str,tk)),al,str(n-6),str(n+6),"12","3","7"],capture_output=True,text=True).stdout.strip()
        print(name,kn,out[:200]); sys.stdout.flush()
