"""Regenerate every verified decrypt from the raw transcriptions. Run from src/:  python3 verify.py"""
from core2 import *
from adfgvx import clean
from messages import MSGS
KEYD["CHI-Nov13"]=([3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16],"AROT+WH++C++SVU+I+DXBP+++JXNZELFK+G+")
KEYD["TRUPPENVERSCHIEBUNG"]=([16,13,17,11,12,3,9,19,4,14,15,2,7,8,5,1,18,10,6],"TRUPE4N+SC2H+I+++G6A+D+F+++KL+O+WX+Z")
def show(name,kn,ct,note):
    tk,al=KEYD[kn]; pt=decrypt(ct,tk,al); print(f"== Childs p.{name}  key={kn}  fix: {note}\n   score={score(pt):.2f}\n   {pt}\n")
show("100","Nov1-3",clean(MSGS["p100"]).replace("FGDDFGDAVGAA","DGFGDDFGDAVGAA"),"insert DG in group 23")
g=MSGS["p105"].split(); g[9]=g[9].replace("X","",1); g[19]=g[19].replace("DG",""); show("105","Nov1-3","".join(g),"drop X grp10, drop DG grp20")
g=MSGS["p109"].split(); g[15:19]=["XXAVV","XXDDG"]; show("109","Nov1-3","".join(g),"groups 16-19 -> XXAVV XXDDG")
tk,al=KEYD["Nov4-6"]; b=untranspose(expand_dashes(MSGS["p132"]),tk); b=b[:57]+b[58:]
print(f"== Childs p.132  key=Nov4-6  fix: delete 1 V from INTERIM text (clerk error)\n   {unsubst(b,al)}\n")
g=MSGS["p146"].split(); g.insert(9,"FVXAA"); i=g.index("XAAXV",44); g[i:i+2]=["XAAXX"]; show("146","Nov4-6","".join(g),"insert FVXAA before grp10; XAAXV XAFDX -> XAAXX")
ct="AAVGF DDADX XDAAV GXAGX AFVAA ADDXD AXDDD DGDDD AAGDV XGVXD GDVDV GVVVV VVGXV VDFVG GVVDV DDVGX DVXVX XGAXA XDDDX XDDXD XXAXD VDXFX ADAGD AGXGA ADDFX XGXDD GDFFA XGDDX XDVVD VVXDF GVVDG VGVAG VXXVV VVVVD VXVGG VGGXG GVVGD GXXVG GVVXX DXDDG VDVVV DDDGG XVVGD DXXDD GGVDX XVVVD GGXGV DGVFA DDDAX DDDAA ADDGD VGDDX XVDVD DVVDV XGVGX XVXXV XXGVA GAGFD XDDAD AXGXD AXXAV DXXGX DXAX"
show("171","Nov7-9",clean(ct),"7 single-symbol edits (Biermann)")
g=expand_dashes(MSGS["p215"]); gs=[g[i:i+5] for i in range(0,len(g),5)]; gs.insert(6,"?????"); gs.insert(44,"?????")
show("215 ('page ??')","Nov22-24","".join(gs),"insert unknown group after grp 6 and grp 43")
show("187 (1 TL)","CHI-Nov13",expand_dashes(MSGS["p187"]),"none")
show("187 (2 TL, 'page ???')","CHI-Nov13",expand_dashes(MSGS["p187b"]),"none")
show("217","TRUPPENVERSCHIEBUNG",expand_dashes(MSGS["p217"]),"none (out-of-period keyword)")
