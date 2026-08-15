// Search directly over A, tracking used primes as a bitmask.
// Covers ALL prime sets simultaneously; outputs E1(k) for every k at once.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int X, KMAX;
static u64 pf[600];              // pf[s] = bitmask of prime factors of s
static int primes[64], np;
static int bestAll[70];          // bestAll[k] = best |A| using <= k primes
static int bestA[70][64];        // witness
static int cur[64];

static inline int pc(u64 x){ return __builtin_popcountll(x); }

static void rec(int size, int last, u64 mask){
    int p = pc(mask);
    if(size > bestAll[p]){
        for(int q=p;q<=KMAX;q++) if(size>bestAll[q]){
            bestAll[q]=size; memcpy(bestA[q],cur,sizeof(int)*size);
        }
    }
    for(int b=last+1;b<=X;b++){
        if(size + (X-b+1) <= bestAll[p]) return;   // monotone prune
        u64 nm = mask;
        for(int i=0;i<size;i++) nm |= pf[cur[i]+b];
        if(pc(nm) > KMAX) continue;
        cur[size]=b;
        rec(size+1,b,nm);
    }
}

int main(int argc,char**argv){
    X=atoi(argv[1]); KMAX=atoi(argv[2]);
    int S=2*X+1;
    // sieve primes up to S
    char *comp=calloc(S+1,1); np=0;
    for(int i=2;i<=S;i++){ if(!comp[i]){ primes[np]=i; if(np<63) np++; for(int j=2*i;j<=S;j+=i) comp[j]=1; } }
    if(np>63){ printf("too many primes (%d) for 64-bit mask; lower X\n",np); return 1; }
    for(int s=1;s<=S;s++){ u64 m=0; int t=s;
        for(int i=0;i<np;i++){ if(t%primes[i]==0){ m|=1ULL<<i; while(t%primes[i]==0)t/=primes[i]; } if(t==1)break; }
        pf[s]=m; }
    memset(bestAll,0,sizeof(bestAll));
    printf("X=%d  primes<=%d: %d  KMAX=%d\n",X,S,np,KMAX);
    rec(0,0,0ULL);
    for(int k=1;k<=KMAX;k++){
        printf("E1(%2d) >= %2d   A =",k,bestAll[k]);
        for(int i=0;i<bestAll[k];i++)printf(" %d",bestA[k][i]);
        printf("\n");
    }
    return 0;
}
