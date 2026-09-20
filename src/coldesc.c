// Coordinate descent over per-column start offsets (readout order). usage: ./coldesc <ct> <key> <alpha> <Nmin> <Nmax> <restarts> <seed> [maxoff]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float Q[26*26*26*26];
static const char SYM[]="ADFGVX"; static double PEN=-7.0;
int K; int key[32]; int order[32]; char alpha[37];
int symidx(char c){ const char*p=strchr(SYM,c); return (p&&c)? (int)(p-SYM): -1; }
double score(const char*pt,int L){ double t=0; int c=0; for(int i=0;i+3<L;i++){ int idx=0,ok=1; for(int j=0;j<4;j++){char ch=pt[i+j]; if(ch<'a'||ch>'z'){ok=0;break;} idx=idx*26+(ch-'a');} if(!ok){t+=PEN;c++;continue;} t+=Q[idx]; c++; } return c? t/c : -99; }
const char*ct; int n;
int lens[32], nom[32];
int build(int N,int*off,char*pt){
    int rows=N/K;
    static char b[4096]; int m=0;
    for(int r=0;r<=rows;r++) for(int i=0;i<K;i++) if(r<lens[i]){ int p=nom[i]+off[i]+r; b[m++]=(p>=0&&p<n)?ct[p]:'?'; }
    int L=0;
    for(int i=0;i+1<m;i+=2){ int x=symidx(b[i]), y=symidx(b[i+1]); if(x<0||y<0){pt[L++]='?';continue;} char ch=alpha[x*6+y]; pt[L++]=(ch=='+')?'?':((ch>='A'&&ch<='Z')?ch+32:ch); }
    pt[L]=0; return L;
}
int main(int argc,char**argv){
    FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"../data/quad.bin","rb"); fread(Q,sizeof(float),26*26*26*26,f); fclose(f);
    ct=argv[1]; n=strlen(ct);
    char*ks=strdup(argv[2]); K=0; for(char*t=strtok(ks,",");t;t=strtok(NULL,",")) key[K++]=atoi(t);
    for(int i=0;i<K;i++) order[i]=i;
    for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(key[order[j]]<key[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    strcpy(alpha,argv[3]); int Nmin=atoi(argv[4]),Nmax=atoi(argv[5]),restarts=atoi(argv[6]); srand(atoi(argv[7])); int MAXD=argc>8?atoi(argv[8]):6;
    double gbest=-99; int goff[32]; int gN=0; char gpt[2048]; char pt[2048];
    for(int N=Nmin;N<=Nmax;N++){
        int rows=N/K, extra=N%K;
        for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
        int pos=0; for(int oi=0;oi<K;oi++){ int i=order[oi]; nom[i]=pos; pos+=lens[i]; }
        for(int rs=0;rs<restarts;rs++){
            int off[32]; for(int i=0;i<K;i++) off[i]= rs==0?0:(rand()%(2*MAXD+1)-MAXD);
            int L=build(N,off,pt); double cur=score(pt,L); double best=cur; int boff[32]; memcpy(boff,off,sizeof(off));
            int ITER=30000;
            for(int it=0;it<ITER;it++){
                double T=0.25*(1.0-(double)it/ITER)+0.01;
                int save[32]; memcpy(save,off,sizeof(save));
                int mv=rand()%4;
                if(mv<2){ int i=rand()%K; off[i]=rand()%(2*MAXD+1)-MAXD; }
                else if(mv==2){ int j=rand()%K; int d=(rand()%2)?1:-1; int ok=1; for(int oi=j;oi<K;oi++){ int i=order[oi]; off[i]+=d; if(abs(off[i])>MAXD) ok=0; } if(!ok){memcpy(off,save,sizeof(save)); continue;} }
                else { int j=rand()%K; int j2=rand()%K; if(j>j2){int t=j;j=j2;j2=t;} int d=(rand()%2)?1:-1; int ok=1; for(int oi=j;oi<=j2;oi++){ int i=order[oi]; off[i]+=d; if(abs(off[i])>MAXD) ok=0; } if(!ok){memcpy(off,save,sizeof(save)); continue;} }
                L=build(N,off,pt); double sc=score(pt,L);
                if(sc>=cur || (rand()/(RAND_MAX+1.0))<exp((sc-cur)/T)){ cur=sc; if(sc>best){best=sc; memcpy(boff,off,sizeof(off));} }
                else memcpy(off,save,sizeof(save));
            }
            memcpy(off,boff,sizeof(off)); cur=best;
            int improved=1;
            while(improved){ improved=0;
                for(int oi=0;oi<K;oi++){ int i=order[oi]; int bo=off[i]; double bs=cur;
                    for(int d=-MAXD;d<=MAXD;d++){ if(d==off[i]) continue; int o=off[i]; off[i]=d; L=build(N,off,pt); double s2=score(pt,L); if(s2>bs){bs=s2;bo=d;} off[i]=o; }
                    if(bs>cur+1e-9){ off[i]=bo; cur=bs; improved=1; }
                }
                for(int j=0;j<K;j++) for(int j2=j;j2<K;j2++) for(int d=-2;d<=2;d++){ if(!d) continue; int ok=1; int save[32]; memcpy(save,off,sizeof(save));
                    for(int oi=j;oi<=j2;oi++){ int i=order[oi]; off[i]+=d; if(abs(off[i])>MAXD) ok=0; }
                    if(ok){ L=build(N,off,pt); double s2=score(pt,L); if(s2>cur+1e-9){cur=s2; improved=1; continue;} }
                    memcpy(off,save,sizeof(save)); }
            }
            if(cur>gbest){ gbest=cur; memcpy(goff,off,sizeof(off)); gN=N; build(N,goff,gpt); }
        }
    }
    printf("%.4f N=%d ",gbest,gN);
    for(int oi=0;oi<K;oi++) printf("%+d,",goff[order[oi]]);
    printf(" %s\n",gpt);
}
