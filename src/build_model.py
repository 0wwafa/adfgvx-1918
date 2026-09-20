"""Rebuild data/quad.bin (German quadgram log10 model).
Downloads a few German Gutenberg texts and mixes in data/military_vocab.txt (up-weighted)."""
import os, re, math, array, urllib.request
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(HERE,"..","data")
IDS=[22367,2407,6099,5323,21000,34811,24571]
txt=""
for i in IDS:
    try: txt+=urllib.request.urlopen(f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt",timeout=60).read().decode("utf-8","ignore")
    except Exception as e: print("skip",i,e)
txt+=open(os.path.join(DATA,"military_vocab.txt"),encoding="utf-8").read()
txt=txt.lower().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
txt=re.sub(r"[^a-z]","",txt)
cnt=Counter(txt[i:i+4] for i in range(len(txt)-3)); tot=sum(cnt.values()); floor=math.log10(0.01/tot)
arr=array.array('f',[floor]*(26**4))
for k,v in cnt.items():
    idx=0
    for c in k: idx=idx*26+ord(c)-97
    arr[idx]=math.log10(v/tot)
arr.tofile(open(os.path.join(DATA,"quad.bin"),"wb")); print("wrote quad.bin, floor",floor)
