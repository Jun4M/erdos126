"""
INDEPENDENT verification (second implementation) of E1(k) and E2(k).

Deliberately different from the C code:
  - Python, not C
  - graph built as explicit adjacency bitmasks over ALL vertices
    (the C code restricts candidates to Smooth - a1)
  - Tomita-style max clique with GREEDY COLORING bound
    (the C code uses only a size bound)
  - smoothness tested by trial division, not by sieving a smooth set
"""
import sys
from math import gcd
from sympy import primerange

def is_smooth(n, S):
    for p in S:
        while n % p == 0:
            n //= p
    return n == 1

def build(X, S, mode):
    """mode 0 = E1 (a+b);  mode 1 = E2 ((a+b)/gcd)."""
    adj = [0]*(X+1)
    for a in range(1, X+1):
        for b in range(a+1, X+1):
            v = a+b
            if mode: v //= gcd(a, b)
            if is_smooth(v, S):
                adj[a] |= 1 << b
                adj[b] |= 1 << a
    return adj

BEST = 0; BESTSET = []

def expand(R, P, adj):
    """Tomita max clique with greedy colouring bound."""
    global BEST, BESTSET
    if not P:
        if len(R) > BEST:
            BEST = len(R); BESTSET = list(R)
        return
    order = []; colour = []
    unc = P; c = 0
    while unc:
        c += 1
        avail = unc
        while avail:
            lb = avail & -avail
            v = lb.bit_length()-1
            avail ^= lb
            avail &= ~adj[v]
            unc ^= lb
            order.append(v); colour.append(c)
    for i in range(len(order)-1, -1, -1):
        if len(R) + colour[i] <= BEST:
            return
        v = order[i]
        expand(R+[v], P & adj[v], adj)
        P &= ~(1 << v)

def maxclique(X, S, mode):
    global BEST, BESTSET
    BEST = 0; BESTSET = []
    adj = build(X, S, mode)
    P = 0
    for v in range(1, X+1):
        if adj[v]: P |= 1 << v
    sys.setrecursionlimit(10000)
    expand([], P, adj)
    return BEST, sorted(BESTSET)

if __name__ == "__main__":
    mode = int(sys.argv[1]); X = int(sys.argv[2])
    S = [int(x) for x in sys.argv[3:]]
    n, A = maxclique(X, S, mode)
    print(f"{'E2' if mode else 'E1'} S={S} X={X} -> {n}   A={A}")
