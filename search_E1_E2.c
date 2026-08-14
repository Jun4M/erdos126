// E1(k) and E2(k) in Wu's notation.
// E1: edge iff (a+b) is S-smooth.  E2: edge iff (a+b)/gcd(a,b) is S-smooth.
#include <stdio.h>
#include <stdlib.h>
static unsigned char *issm; static long SMAX;
static int MODE; // 0 = E1, 1 = E2
static long gcdl(long a,long b){while(b){long t=a%b;a=b;b=t;}return a;}
static inline int ok(long a,long b){
    long s=a+b; if(MODE) s/=gcdl(a,b);
    return s<=SMAX && issm[s];
}
static int best; static long cur[64],bs[64];
static void dfs(int d,long*C,int m){
    if(d>best){best=d; for(int i=0;i<d;i++)bs[i]=cur[i];}
    for(int i=0;i<m;i++){ if(d+(m-i)<=best)return;
        long v=C[i]; cur[d]=v;
        long*C2=malloc(sizeof(long)*(m-i)); int m2=0;
        for(int j=i+1;j<m;j++) if(ok(v,C[j]))C2[m2++]=C[j];
        dfs(d+1,C2,m2); free(C2); }
}
int main(int argc,char**argv){
    MODE=atoi(argv[1]); long X=atol(argv[2]); int k=argc-3; long P[24];
    for(int i=0;i<k;i++)P[i]=atol(argv[3+i]);
    SMAX=2*X+2; issm=calloc(SMAX+1,1);
    long cap=1L<<22; long*cl=malloc(sizeof(long)*cap); long c=1; cl[0]=1;
    for(int i=0;i<k;i++){ long*nl=malloc(sizeof(long)*cap); long nc=0;
        for(long j=0;j<c;j++){ long v=cl[j];
            while(v<=SMAX){ nl[nc++]=v; if(v>SMAX/P[i])break; v*=P[i]; } }
        free(cl); cl=nl; c=nc; }
    for(long j=0;j<c;j++) issm[cl[j]]=1;
    best=0; long*C=malloc(sizeof(long)*(X+2));
    for(long a1=1;a1<=X;a1++){ int m=0;
        for(long b=a1+1;b<=X;b++) if(ok(a1,b))C[m++]=b;
        if(1+m<=best)continue; cur[0]=a1; dfs(1,C,m); }
    printf("%s k=%d X=%ld : %d   A=",MODE?"E2":"E1",k,X,best);
    for(int i=0;i<best;i++)printf(" %ld",bs[i]);
    printf("\n"); return 0;
}
