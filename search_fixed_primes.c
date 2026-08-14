// g(k) lower bounds: largest A subset [1,LIM] with all pairwise sums S-smooth.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned char *issm;   // issm[x] = 1 if x is S-smooth
static long LIM, SMAX;
static int best;
static long bestset[64];
static long cur[64];

static void dfs(int depth, long *C, int m) {
    if (depth > best) {
        best = depth;
        memcpy(bestset, cur, sizeof(long)*depth);
    }
    for (int i = 0; i < m; i++) {
        if (depth + (m - i) <= best) return;      // prune
        long v = C[i];
        cur[depth] = v;
        long *C2 = malloc(sizeof(long)*(m - i));
        int m2 = 0;
        for (int j = i+1; j < m; j++)
            if (issm[v + C[j]]) C2[m2++] = C[j];
        dfs(depth+1, C2, m2);
        free(C2);
    }
}

int main(int argc, char **argv) {
    // argv: LIM p1 p2 ...
    LIM = atol(argv[1]);
    SMAX = 2*LIM;
    int k = argc - 2;
    long P[16];
    for (int i = 0; i < k; i++) P[i] = atol(argv[2+i]);

    issm = calloc(SMAX+1, 1);
    // sieve of smooth numbers
    long *cur_list = malloc(sizeof(long)*(SMAX+2));
    long cnt = 1; cur_list[0] = 1;
    for (int i = 0; i < k; i++) {
        long *nl = malloc(sizeof(long)*(SMAX+2));
        long nc = 0;
        for (long j = 0; j < cnt; j++) {
            for (long v = cur_list[j]; v <= SMAX; v *= P[i]) {
                nl[nc++] = v;
                if (v > SMAX / P[i]) break;
            }
        }
        free(cur_list); cur_list = nl; cnt = nc;
    }
    for (long j = 0; j < cnt; j++) issm[cur_list[j]] = 1;

    long *sm = malloc(sizeof(long)*cnt);
    long ns = 0;
    for (long x = 1; x <= SMAX; x++) if (issm[x]) sm[ns++] = x;

    best = 0;
    long *C = malloc(sizeof(long)*(ns+2));
    for (long a1 = 1; a1 <= LIM; a1++) {
        int m = 0;
        for (long t = 0; t < ns; t++) {
            long b = sm[t] - a1;
            if (b > a1 && b <= LIM) C[m++] = b;
        }
        if (1 + m <= best) continue;
        cur[0] = a1;
        dfs(1, C, m);
    }
    printf("LIM=%ld  primes=", LIM);
    for (int i = 0; i < k; i++) printf("%ld%s", P[i], i==k-1?"":",");
    printf("  |A|=%d  A=", best);
    for (int i = 0; i < best; i++) printf("%ld%s", bestset[i], i==best-1?"":",");
    printf("  (#smooth<=%ld: %ld)\n", SMAX, ns);
    return 0;
}
