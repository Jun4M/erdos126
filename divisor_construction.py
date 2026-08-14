#!/usr/bin/env python3
"""
Divisor-set constructions for E2.

Lemma. Let A = the set of all divisors of n. For d, d' in A with g = gcd(d,d'),
       (d + d')/g = u + v where u = d/g, v = d'/g are COPRIME divisors of n
       with uv | n.  Hence

           (A ^+ A)' = { u+v : u,v | n, gcd(u,v)=1, uv | n, u != v }.

This collapses C(tau(n),2) conditions down to the number of coprime divisor
pairs, which is why divisor sets do well for E2 (and not for E1, where there
is no division by the gcd).

Corollary (n = 2^a).  A = {1,2,4,...,2^a} gives (A ^+ A)' = {2^m + 1 : 1<=m<=a},
so  E2( omega(prod_{m=1..a} (2^m+1)) ) >= a+1.

WARNING: this family is WEAK. By Zsygmondy, 2^(2m)-1 has a primitive prime
divisor for m > 3, which divides 2^m+1 and no smaller 2^m'+1, so
omega(prod) ~ a and the bound is only linear -- far below the trivial
construction A = {1,...,m}, which gives E1(k) >= (p_{k+1}-1)/2 ~ (k log k)/2.

The construction IS however the source of the smallest known counterexample to
Wu's Problem 1:  n = 63 = 3^2 * 7 gives A = {1,3,7,9,21,63}, |A| = 6, with
(A ^+ A)' = {4,8,10,16,22,64} using only the primes {2,5,11}.  Since E1(3) = 5,
this shows E1(3) != E2(3).
"""
from math import gcd
from sympy import factorint, divisors


def divisor_set_omega(n):
    """Return (tau(n), sorted primes used, sorted distinct values of (d+d')/gcd)."""
    D = divisors(n)
    vals, S = set(), set()
    for i in range(len(D)):
        for j in range(i + 1, len(D)):
            v = (D[i] + D[j]) // gcd(D[i], D[j])
            vals.add(v)
            S |= set(factorint(v))
    return len(D), sorted(S), sorted(vals)


def scan(limit=200000, kmax=8):
    """Best tau(n) achievable for each omega, over n <= limit."""
    best = {}
    for n in range(2, limit):
        D = divisors(n)
        if len(D) < 4:
            continue
        S, ok = set(), True
        for i in range(len(D)):
            for j in range(i + 1, len(D)):
                S |= set(factorint((D[i] + D[j]) // gcd(D[i], D[j])))
                if len(S) > kmax:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        k = len(S)
        if k not in best or len(D) > best[k][0]:
            best[k] = (len(D), n, sorted(S))
    return best


if __name__ == "__main__":
    t, S, vals = divisor_set_omega(63)
    print(f"n = 63:  tau = {t}, primes = {S}, values = {vals}")
    print()
    print("Best divisor sets by omega:")
    for k, (t, n, S) in sorted(scan().items()):
        print(f"  k={k:>2}  tau={t:>3}  n={n:>7}  {factorint(n)}  primes={S}")
