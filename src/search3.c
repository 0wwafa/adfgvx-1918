// Multi-edit search restricted to positions on a grid (step). usage: ./search3 <ct> <key> <alpha> <maxd> <step> <maxedits> <topN> [pen]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float Q[26*26*26*26];
static const char SYM[]="ADFGVX"; static double PEN=-7.0;
int K; int key[32]; int order[32]; char alpha[37];
int symidx(char c){ const char*p=strchr(SYM,c); return (p&&c)? (int)(p-SYM): -1; }
int decrypt(const char*ct,int n,char*pt){
    int rows=n/K, extra=n%K; int lens[32]; int start[32]; int pos=0;
    for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
    for(int oi=0;oi<K;oi++){ int i=order[oi]; start[i]=pos; pos+=lens[i]; }
    static char b[4096]; int m=0;
    for(int r=0;r<=rows;r++) for(int i=0;i<K;i++) if(r<lens[i]) b[m++]=ct[start[i]+r];
    int L=0;
    for(int i=0;i+1<m;i+=2){ int x=symidx(b[i]), y=symidx(b[i+1]); if(x<0||y<0){pt[L++]='?';continue;} char ch=alpha[x*6+y]; pt[L++]=(ch=='+')?'?':((ch>='A'&&ch<='Z')?ch+32:ch); }
    pt[L]=0; return L;
}
double score(const char*pt,int L){ double t=0; int c=0; for(int i=0;i+3<L;i++){ int idx=0,ok=1; for(int j=0;j<4;j++){char ch=pt[i+j]; if(ch<'a'||ch>'z'){ok=0;break;} idx=idx*26+(ch-'a');} if(!ok){t+=PEN;c++;continue;} t+=Q[idx]; c++; } return c? t/c : -99; }
typedef struct{double s;int ne;int p[4],d[4];} Res;
int cmp(const void*a,const void*b){ double x=((Res*)a)->s,y=((Res*)b)->s; return x<y?1:(x>y?-1:0);}
Res *res; int nr=0, topN; double thresh=-1e9;
const char*ct; int n; int maxd, step, maxedits;
void record(double s,int ne,int*p,int*d){
    Res r; r.s=s; r.ne=ne; for(int i=0;i<ne;i++){r.p[i]=p[i];r.d[i]=d[i];}
    if(nr<topN){res[nr++]=r; if(nr==topN){thresh=1e9; for(int i=0;i<nr;i++) if(res[i].s<thresh) thresh=res[i].s;}}
    else if(s>thresh){ int w=0; for(int i=1;i<nr;i++) if(res[i].s<res[w].s) w=i; res[w]=r; thresh=1e9; for(int i=0;i<nr;i++) if(res[i].s<thresh) thresh=res[i].s; }
}
void applyall(int ne,int*p,int*d,char*out,int*on){
    // edits sorted by position ascending, non-overlapping. Build left to right.
    int m=0, i=0, e=0;
    while(i<=n){
        if(e<ne && p[e]==i){ if(d[e]>0){ for(int j=0;j<d[e];j++) out[m++]='?'; } else { i+=-d[e]; e++; continue; } e++; continue; }
        if(i<n) out[m++]=ct[i];
        i++;
    }
    out[m]=0; *on=m;
}
char out[4096], pt[2048];
void rec(int ne,int*p,int*d,int minpos){
    int on; applyall(ne,p,d,out,&on); int L=decrypt(out,on,pt); double s=score(pt,L); record(s,ne,p,d);
    if(ne==maxedits) return;
    for(int pos=minpos;pos<=n;pos+=step){
        for(int dd=-maxd;dd<=maxd;dd++){ if(dd==0) continue; if(dd<0 && pos-dd>n) continue; if(pos==n && dd<0) continue;
            p[ne]=pos; d[ne]=dd; rec(ne+1,p,d,pos+(dd<0?-dd:step)); }
    }
}
int main(int argc,char**argv){
    FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"../data/quad.bin","rb"); fread(Q,sizeof(float),26*26*26*26,f); fclose(f);
    ct=argv[1]; n=strlen(ct);
    char*ks=strdup(argv[2]); K=0; for(char*t=strtok(ks,",");t;t=strtok(NULL,",")) key[K++]=atoi(t);
    for(int i=0;i<K;i++) order[i]=i;
    for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(key[order[j]]<key[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    strcpy(alpha,argv[3]); maxd=atoi(argv[4]); step=atoi(argv[5]); maxedits=atoi(argv[6]); topN=atoi(argv[7]); if(argc>8) PEN=atof(argv[8]);
    res=malloc(sizeof(Res)*(topN+1));
    int p[4],d[4]; rec(0,p,d,0);
    qsort(res,nr,sizeof(Res),cmp);
    for(int i=0;i<nr;i++){ int on; applyall(res[i].ne,res[i].p,res[i].d,out,&on); int L=decrypt(out,on,pt); printf("%.4f",res[i].s); for(int j=0;j<res[i].ne;j++) printf(" %d:%+d",res[i].p[j],res[i].d[j]); printf(" | %s\n",pt); }
}
