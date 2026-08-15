#!/usr/bin/env python3
"""
Independent re-verification of every witness set listed in data.txt.
Uses no clique code: each pairwise value is factored from scratch.
Checks cardinality, omega, gcd = 1 and distinctness against the claim.
"""
import re, sys
from math import gcd
from functools import reduce
from sympy import factorint

def check(path="data.txt"):
    txt = open(path).read()
    sec2 = txt.index("# E2(k)")
    ok, n = True, 0
    for line in txt.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        head = re.match(r'^(\d+)\s+(\d+)\s', line)
        if not head:
            continue
        k, claim = int(head.group(1)), int(head.group(2))
        # the witness is the LAST bare comma-separated run of digits on the line
        runs = re.findall(r'(?<![{\d,])\d+(?:,\d+)+(?![,\d}])', line)
        if not runs:
            continue
        A = [int(x) for x in runs[-1].split(',')]
        use_gcd = txt.index(line) > sec2
        S = set()
        for i in range(len(A)):
            for j in range(i+1, len(A)):
                v = A[i] + A[j]
                if use_gcd:
                    v //= gcd(A[i], A[j])
                S |= set(factorint(v))
        good = (len(S) == k and len(A) == claim
                and reduce(gcd, A) == 1 and len(A) == len(set(A)))
        tag = "E2" if use_gcd else "E1"
        print(f"  {tag} k={k:>2}  |A|={len(A):>3} (claim {claim:>3})  "
              f"omega={len(S):>3}  {'OK' if good else 'FAIL'}")
        ok &= good; n += 1
    print(f"\n{n} witness sets checked -> {'ALL PASS' if ok else 'FAILURES'}")
    return ok

if __name__ == "__main__":
    sys.exit(0 if check(*sys.argv[1:]) else 1)
