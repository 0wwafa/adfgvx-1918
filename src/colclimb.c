// Column-offset simulated annealing for ADFGVX with known key.
// usage: ./colclimb <ct> <key> <alpha> <Nmin> <Nmax> <restarts> <seed>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float Q[26*26*26*26];
static const char SYM[]="ADFGVX"; static double PEN=-7.0;
int K; int key[32]; int order[32]; char alpha[37];
int symidx(char c){ const char*p=strchr(SYM,c); return (p&&c)? (int)(p-SYM): -1; }
double score(const char*pt,int L){ double t=0; int c=0; for(int i=0;i+3<L;i++){ int idx=0,ok=1; for(int j=0;j<4;j++){char ch=pt[i+j]; if(ch<'a'||ch>'z'){ok=0;break;} idx=idx*26+(ch-'a');} if(!ok){t+=PEN;c++;continue;} t+=Q[idx]; c++; } return c? t/c : -99; }
// build plaintext from column starts
int build(const char*ct,int n,int N,int*start,char*pt){
    int rows=N/K, extra=N%K; int lens[32];
    for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
    static char b[4096]; int m=0;
    for(int r=0;r<=rows;r++) for(int i=0;i<K;i++) if(r<lens[i]){ int p=start[i]+r; b[m++]=(p>=0&&p<n)?ct[p]:'?'; }
    int L=0;
    for(int i=0;i+1<m;i+=2){ int x=symidx(b[i]), y=symidx(b[i+1]); if(x<0||y<0){pt[L++]='?';continue;} char ch=alpha[x*6+y]; pt[L++]=(ch=='+')?'?':((ch>='A'&&ch<='Z')?ch+32:ch); }
    pt[L]=0; return L;
}
double rnd(){ return rand()/(RAND_MAX+1.0); }
int main(int argc,char**argv){
    FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"../data/quad.bin","rb"); fread(Q,sizeof(float),26*26*26*26,f); fclose(f);
    const char*ct=argv[1]; int n=strlen(ct);
    char*ks=strdup(argv[2]); K=0; for(char*t=strtok(ks,",");t;t=strtok(NULL,",")) key[K++]=atoi(t);
    for(int i=0;i<K;i++) order[i]=i;
    for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(key[order[j]]<key[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    strcpy(alpha,argv[3]); int Nmin=atoi(argv[4]),Nmax=atoi(argv[5]),restarts=atoi(argv[6]); srand(atoi(argv[7]));
    int MAXD=8;
    double gbest=-99; int gstart[32]; int gN=0; char gpt[2048];
    for(int N=Nmin;N<=Nmax;N++){
        int rows=N/K, extra=N%K; int lens[32], nom[32];
        for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
        int pos=0; for(int oi=0;oi<K;oi++){ int i=order[oi]; nom[i]=pos; pos+=lens[i]; }
        for(int rs=0;rs<restarts;rs++){
            int st[32]; for(int i=0;i<K;i++) st[i]=nom[i]+ (rand()%3-1);
            char pt[2048]; int L=build(ct,n,N,st,pt); double cur=score(pt,L); double best=cur; int bst[32]; memcpy(bst,st,sizeof(st));
            double T=0.3;
            for(int it=0;it<20000;it++){
                int i=rand()%K; int old=st[i]; int d=(rand()%(2*MAXD+1))-MAXD; int mv=rand()%3;
                int oldall[32]; memcpy(oldall,st,sizeof(st));
                if(mv==0){ st[i]=nom[i]+d; }
                else if(mv==1){ int sh=(rand()%2)?1:-1; for(int oi=0;oi<K;oi++){ int j=order[oi]; if(oi>=0) ; } // shift all columns after i in readout order
                    int found=0; for(int oi=0;oi<K;oi++){ int j=order[oi]; if(j==i) found=1; if(found){ st[j]+=sh; if(abs(st[j]-nom[j])>MAXD) st[j]-=sh; } } }
                else { st[i]=old+((rand()%2)?1:-1); if(abs(st[i]-nom[i])>MAXD) st[i]=old; }
                L=build(ct,n,N,st,pt); double s=score(pt,L);
                if(s>=cur || rnd()<exp((s-cur)/T)){ cur=s; if(s>best){best=s; memcpy(bst,st,sizeof(st));} }
                else memcpy(st,oldall,sizeof(st));
                T=0.3*(1.0-(double)it/20000)+0.005;
            }
            if(best>gbest){ gbest=best; memcpy(gstart,bst,sizeof(bst)); gN=N; build(ct,n,N,bst,gpt); }
        }
    }
    printf("%.4f N=%d ",gbest,gN);
    { int rows=gN/K, extra=gN%K; int pos=0; for(int oi=0;oi<K;oi++){ int i=order[oi]; printf("%+d,",gstart[i]-pos); pos+=rows+(i<extra);} }
    printf(" %s\n",gpt);
}
