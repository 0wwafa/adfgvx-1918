// Two-edit search for ADFGVX with known key. Usage: ./search2 <ct with ?> <keystring comma> <alpha36> <maxd> <topN>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float Q[26*26*26*26];
static const char SYM[]="ADFGVX"; static double PEN=-7.0;
int K; int key[32]; int order[32]; char alpha[37];
int symidx(char c){ const char*p=strchr(SYM,c); return p? (int)(p-SYM): -1; }
// decrypt ct (len n) into pt; returns pt length
int decrypt(const char*ct,int n,char*pt){
    int rows=n/K, extra=n%K; int lens[32]; int start[32]; int pos=0;
    for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
    for(int oi=0;oi<K;oi++){ int i=order[oi]; start[i]=pos; pos+=lens[i]; }
    static char b[4096]; int m=0;
    for(int r=0;r<=rows;r++) for(int i=0;i<K;i++) if(r<lens[i]) b[m++]=ct[start[i]+r];
    int L=0;
    for(int i=0;i+1<m;i+=2){ int x=symidx(b[i]), y=symidx(b[i+1]); if(x<0||y<0){pt[L++]='?';continue;} char ch=alpha[x*6+y]; pt[L++]= (ch=='+')?'?':((ch>='A'&&ch<='Z')?ch+32:ch); }
    pt[L]=0; return L;
}
double score(const char*pt,int L){ double t=0; int c=0; for(int i=0;i+3<L;i++){ int idx=0,ok=1; for(int j=0;j<4;j++){char ch=pt[i+j]; if(ch<'a'||ch>'z'){ok=0;break;} idx=idx*26+(ch-'a');} if(!ok){t+=PEN;c++;continue;} t+=Q[idx]; c++; } return c? t/c : -99; }
typedef struct{double s;int p1,d1,p2,d2;} Res;
int cmp(const void*a,const void*b){ double x=((Res*)a)->s,y=((Res*)b)->s; return x<y?1:(x>y?-1:0);}
void apply(const char*ct,int n,int p1,int d1,int p2,int d2,char*out,int*on){
    // apply at p2 then p1 (p1<=p2). Edits: d>0 insert d '?', d<0 delete -d chars
    char tmp[4096]; int m=0;
    for(int i=0;i<n;i++){ if(i==p2){ if(d2>0) for(int j=0;j<d2;j++) tmp[m++]='?'; } if(i>=p2 && i<p2-d2 && d2<0) continue; tmp[m++]=ct[i]; }
    if(p2==n && d2>0) for(int j=0;j<d2;j++) tmp[m++]='?';
    int mm=0;
    for(int i=0;i<m;i++){ if(i==p1){ if(d1>0) for(int j=0;j<d1;j++) out[mm++]='?'; } if(i>=p1 && i<p1-d1 && d1<0) continue; out[mm++]=tmp[i]; }
    if(p1==m && d1>0) for(int j=0;j<d1;j++) out[mm++]='?';
    out[mm]=0; *on=mm;
}
int main(int argc,char**argv){
    FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"../data/quad.bin","rb"); fread(Q,sizeof(float),26*26*26*26,f); fclose(f);
    const char*ct=argv[1]; int n=strlen(ct);
    char*ks=strdup(argv[2]); K=0; for(char*t=strtok(ks,",");t;t=strtok(NULL,",")) key[K++]=atoi(t);
    // order: sort columns by key value
    for(int i=0;i<K;i++) order[i]=i;
    for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(key[order[j]]<key[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    strcpy(alpha,argv[3]); int maxd=atoi(argv[4]); int topN=atoi(argv[5]);
    int two = argc>6 ? atoi(argv[6]) : 1;
    Res *res=malloc(sizeof(Res)*200000); int nr=0; Res worst; double thresh=-1e9;
    char out[4096], pt[2048]; int on;
    // single edits & none
    for(int p1=0;p1<=n;p1++) for(int d1=-maxd;d1<=maxd;d1++){
        if(p1==n && d1<0) continue; if(d1<0 && p1-d1>n) continue;
        if(p1>0 && d1==0) continue;
        apply(ct,n,p1,d1,n,0,out,&on); int L=decrypt(out,on,pt); double s=score(pt,L);
        if(nr<topN){res[nr++]=(Res){s,p1,d1,-1,0};} else { if(s>thresh){ int w=0; for(int i=1;i<nr;i++) if(res[i].s<res[w].s) w=i; res[w]=(Res){s,p1,d1,-1,0}; thresh=1e9; for(int i=0;i<nr;i++) if(res[i].s<thresh) thresh=res[i].s; } }
    }
    if(two) for(int p1=0;p1<=n;p1++) for(int d1=-maxd;d1<=maxd;d1++){ if(d1==0) continue; if(d1<0 && p1-d1>n) continue;
      for(int p2=p1+(d1<0?-d1:1);p2<=n;p2++) for(int d2=-maxd;d2<=maxd;d2++){ if(d2==0) continue; if(d2<0 && p2-d2>n) continue;
        apply(ct,n,p1,d1,p2,d2,out,&on); int L=decrypt(out,on,pt); double s=score(pt,L);
        if(nr<topN){res[nr++]=(Res){s,p1,d1,p2,d2}; if(nr==topN){thresh=1e9; for(int i=0;i<nr;i++) if(res[i].s<thresh) thresh=res[i].s;}}
        else if(s>thresh){ int w=0; for(int i=1;i<nr;i++) if(res[i].s<res[w].s) w=i; res[w]=(Res){s,p1,d1,p2,d2}; thresh=1e9; for(int i=0;i<nr;i++) if(res[i].s<thresh) thresh=res[i].s; }
      }}
    qsort(res,nr,sizeof(Res),cmp);
    for(int i=0;i<nr;i++){ apply(ct,n,res[i].p1,res[i].d1,res[i].p2<0?n:res[i].p2,res[i].d2,out,&on); int L=decrypt(out,on,pt); printf("%.4f p1=%d d1=%d p2=%d d2=%d %s\n",res[i].s,res[i].p1,res[i].d1,res[i].p2,res[i].d2,pt); }
}
