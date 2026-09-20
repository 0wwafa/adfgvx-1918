// Unknown-transposition attack: SA over permutation, fitness = bigram IC of interim text (+ row/col asymmetry).
// usage: ./transclimb <ct> <Kmin> <Kmax> <restarts> <seed>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static const char SYM[]="ADFGVX";
const char*ct; int n;
int sidx(char c){ const char*p=strchr(SYM,c); return (p&&c)?(int)(p-SYM):-1; }
// key: perm[i] = original column index read out at position i (readout order)
double fitness(int K,int*perm){
    int rows=n/K, extra=n%K; int lens[32], start[32];
    // column i (original index) has length rows+(i<extra)
    for(int i=0;i<K;i++) lens[i]=rows+(i<extra);
    int pos=0; for(int oi=0;oi<K;oi++){ int i=perm[oi]; start[i]=pos; pos+=lens[i]; }
    static char b[4096]; int m=0;
    for(int r=0;r<=rows;r++) for(int i=0;i<K;i++) if(r<lens[i]) b[m++]=ct[start[i]+r];
    int cnt[36]={0}; int tot=0;
    for(int i=0;i+1<m;i+=2){ int x=sidx(b[i]),y=sidx(b[i+1]); if(x<0||y<0) continue; cnt[x*6+y]++; tot++; }
    double ic=0; for(int i=0;i<36;i++) ic+=cnt[i]*(cnt[i]-1.0); ic/= (tot*(tot-1.0));
    return ic;
}
double rnd(){return rand()/(RAND_MAX+1.0);}
int main(int argc,char**argv){
    ct=argv[1]; n=strlen(ct); int Kmin=atoi(argv[2]),Kmax=atoi(argv[3]),restarts=atoi(argv[4]); srand(atoi(argv[5]));
    for(int K=Kmin;K<=Kmax;K++){
        double gb=-1; int gperm[32];
        for(int rs=0;rs<restarts;rs++){
            int perm[32]; for(int i=0;i<K;i++) perm[i]=i;
            for(int i=K-1;i>0;i--){ int j=rand()%(i+1); int t=perm[i];perm[i]=perm[j];perm[j]=t; }
            double cur=fitness(K,perm), best=cur; int bp[32]; memcpy(bp,perm,sizeof(perm));
            int IT=30000;
            for(int it=0;it<IT;it++){
                double T=0.01*(1.0-(double)it/IT)+0.0005;
                int save[32]; memcpy(save,perm,sizeof(perm));
                int mv=rand()%3;
                if(mv==0){ int i=rand()%K,j=rand()%K; int t=perm[i];perm[i]=perm[j];perm[j]=t; }
                else if(mv==1){ int i=rand()%K,j=rand()%K; if(i>j){int t=i;i=j;j=t;} int t=perm[i]; for(int k=i;k<j;k++) perm[k]=perm[k+1]; perm[j]=t; }
                else { int i=rand()%K,j=rand()%K; if(i>j){int t=i;i=j;j=t;} while(i<j){int t=perm[i];perm[i]=perm[j];perm[j]=t;i++;j--;} }
                double s=fitness(K,perm);
                if(s>=cur || rnd()<exp((s-cur)/T)){ cur=s; if(s>best){best=s; memcpy(bp,perm,sizeof(perm));} }
                else memcpy(perm,save,sizeof(perm));
            }
            if(best>gb){ gb=best; memcpy(gperm,bp,sizeof(bp)); }
        }
        // convert perm (readout order) to rank key: key[col]=rank
        int key[32]; for(int oi=0;oi<K;oi++) key[gperm[oi]]=oi+1;
        printf("K=%d ic=%.4f key=",K,gb); for(int i=0;i<K;i++) printf("%d%s",key[i],i<K-1?",":""); printf("\n"); fflush(stdout);
    }
}
