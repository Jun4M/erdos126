#!/usr/bin/env python3
"""
Exhaustive sweep over k-element prime sets S (always containing 2) for a given k,
calling ./gk (compiled from search_fixed_primes.c) on each.

Usage:  python3 sweep_prime_sets.py K X POOLSIZE
Example: python3 sweep_prime_sets.py 11 300 13
"""
import sys, itertools, subprocess, time

K = int(sys.argv[1]); X = sys.argv[2]; NPOOL = int(sys.argv[3])
ALLP = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
pool = ALLP[:NPOOL]
combos = list(itertools.combinations(pool, K-1))

best = (0, None, None); res = []; t0 = time.time()
for c in combos:
    S = [2] + list(c)
    out = subprocess.run(["./gk", X] + [str(p) for p in S],
                         capture_output=True, text=True).stdout
    n = int(out.split("|A|=")[1].split()[0])
    A = out.split("A=")[1].split()[0]
    res.append((n, tuple(S)))
    if n > best[0]:
        best = (n, S, A)
res.sort(reverse=True)
print(f"k={K}  X={X}  pool={pool}  ({len(combos)} sets)")
print(f"  E1({K}) >= {best[0]}")
print(f"  S = {best[1]}")
print(f"  A = {best[2]}")
print(f"  runner-up: {res[1][0]}  {list(res[1][1])}")
print(f"  {time.time()-t0:.0f}s")
