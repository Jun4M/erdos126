# Erdős Problem #126 — computational search

Code accompanying computed values of

    E1(k) = max { |A| : A a finite set of distinct positive integers,
                  omega( prod_{a != b in A} (a+b) ) <= k }

which is (essentially) the inverse of the function f in
[Erdős Problem #126](https://www.erdosproblems.com/126).

Equivalently E1(k) is the largest size of a set whose pairwise sums are
all S-units for some set S of k primes — an *additive* analogue of the
S-Diophantine tuples of Szalay–Ziegler.

## Values found

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|
| E1(k) | 2 | 4 | 5 | 6 | 8 | 10 | 11 | 14 | 15 | 17 | 20 | 21 | 24 | 26 | 28 | 31 | 32 |

- k = 1, 2 are theorems of Wu (2019).
- k = 3..14: exhaustive over all A in [1,X] **and** over all k-element prime
  sets containing 2, with the pool ranging from {2,3,...,23} to {2,3,...,59}
  depending on k; see `data.txt` for the exact pool, number of sets and search
  bound X at each k.
- k = 15..17: restricted search (first k primes plus single-swap neighbours);
  these are lower bounds.

2 must lie in S once |A| >= 3, since two of any three integers share parity.

## Notable observations

- For every k tested the extremal set uses **exactly** k primes.
- For 1 <= k <= 12 and 14 <= k <= 17 the optimal prime set is {p_1,...,p_k}.
  **At k = 13 it is not**: S = {2,3,5,7,11,13,17,19,23,29,31,37,43} (omitting 41)
  gives 24, whereas the first 13 primes give only 23 — even though the former
  has *fewer* available smooth numbers (1006 vs 1008 up to 3000).

## E2 and Wu's Problem 1

Wu also defines E2(k), the same quantity with (a+b)/gcd(a,b) in place of (a+b),
and asks (Problem 1) whether E1(k) = E2(k) for all k >= 2. Searching
exhaustively over prime sets containing 2 — the pool varies with k, from
{3,...,23} up to {3,...,43}; see `data.txt` for the exact pool, number of sets
and search bound X used at each k — gives

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|----|----|
| E1(k) | 2 | 4 | 5 | 6 | 8 | 10 | 11 | 14 | 15 | 17 | 20 |
| E2(k) | 2 | 4 | 6 | 7 | 8 | 10 | 11 | 14 | 16 | 17 | 20 |

The two differ at k = 3, 4 and 9 but **agree at k = 5, 6, 7, 8, 10, 11** — the
separation is intermittent, with no evident pattern — so
*neither* alternative in Wu's Problem 1 holds — it is not true that
E1(k) = E2(k) for all k >= 2, nor that they always differ. The smallest
counterexample to equality is k = 3:

    A = {1, 3, 7, 9, 21, 63} = divisors of 63,   S = {2, 5, 11}

    (A ^+ A)' = {4, 8, 10, 16, 22, 64}

This is an instance of a general mechanism. If A is the full set of divisors of
n, then for d, d' in A with g = gcd(d,d') we have (d+d')/g = u+v where u, v are
*coprime* divisors of n with uv | n. So

    (A ^+ A)' = { u+v : u,v | n, gcd(u,v)=1, uv | n, u != v },

collapsing C(tau(n),2) conditions to the number of coprime divisor pairs. E1 has
no division by the gcd and so no such collapse — this is why the two functions
separate. See `divisor_construction.py`.

The specialisation n = 2^a gives E2(omega(prod_{m=1..a}(2^m+1))) >= a+1, but this
is only linear in k (by Zsygmondy each 2^m+1 contributes about one new prime), so
it is far weaker than the trivial construction. Divisor sets beat {1,...,m} only
at k = 3.

A second witness for E2(3) = 6 with a different structure is
{35, 49, 77, 175, 275, 385} with S = {2, 3, 31}; and E2(4) = 7 is attained both
by {2,23,46,138,322,598,782} with S = {2,3,5,7} and by {1,7,14,31,49,119,161}
with S = {2,3,5,19}. So the separation is not an isolated accident. At k = 9,
E2(9) = 16 is attained by the all-odd set
{1,3,5,9,13,15,17,21,25,27,29,39,51,63,75,87} with S = {2,3,...,23}, while
E1(9) = 15.

Wu's Problem 3 asks whether E2(k+1) = 2E2(k) for infinitely many k. In the
computed range doubling happens only at k = 1 (2 -> 4).

## Verification

All values were computed twice, by implementations with deliberately different
designs:

| | `search_fixed_primes.c` / `search_E1_E2.c` | `verify_independent.py` |
|---|---|---|
| candidate pool | restricted to `SmoothSet - a1` | none; full adjacency bitmask |
| clique search | DFS with size bound | Tomita with greedy-colouring bound |
| smoothness | lookup in a sieved smooth set | trial division |

28 of 28 values agreed. Separately, `verify_data.py` re-checks every witness
set listed in `data.txt` from scratch — factoring each pairwise value with
sympy, with no clique code involved — against its claimed cardinality, omega
and gcd. This second check caught one transcription error (a spurious 41 in
the k = 13 witness) which is now fixed; all 30 witness sets now pass.

## Files

| file | purpose |
|---|---|
| `search_fixed_primes.c` | max clique for one fixed prime set S; the workhorse |
| `search_all_primes.c` | searches over A directly, tracking used primes as a 64-bit mask; covers all prime sets at once, but scales poorly in X |
| `search_E1_E2.c` | computes both E1 (edge iff a+b is S-smooth) and E2 (edge iff (a+b)/gcd(a,b) is S-smooth) |
| `sweep_prime_sets.py` | exhaustive sweep over k-element prime sets |
| `sweep_neighbourhood.py` | restricted sweep: first k primes plus single-swap neighbours |
| `divisor_construction.py` | divisor-set constructions for E2; source of the k=3 counterexample to Wu's Problem 1 |
| `verify_independent.py` | second, independent max-clique implementation used for cross-checking |
| `verify_data.py` | re-verifies every witness in `data.txt` by direct factorisation |

## Build and run

    gcc -O2 -o gk search_fixed_primes.c
    ./gk 3000 2 3 5 7 11          # X=3000, S={2,3,5,7,11}

    gcc -O2 -o e2 search_E1_E2.c
    ./e2 0 3000 2 3 5 7           # mode 0 = E1
    ./e2 1 3000 2 3 5 7           # mode 1 = E2

    gcc -O2 -o all search_all_primes.c
    ./all 60 13                   # X=60, all k up to 13 at once

    python3 sweep_prime_sets.py 11 300 13

## Method

For a fixed S, the key reduction is: once the smallest element a1 of A is fixed,
every other element lies in (SmoothSet - a1), so the candidate pool shrinks from
X to the number of S-smooth integers below 2X. A depth-first maximum-clique
search on that pool then finishes quickly.

## References

- P. Erdős, P. Turán, *On a problem in the elementary theory of numbers*,
  Amer. Math. Monthly **41** (1934), 608–611.
- P. Erdős, J. Surányi, *Topics in the Theory of Numbers*, Springer, 2003.
- B.-L. Wu, *Sumsets with restricted number of prime factors*,
  Lith. Math. J. **59** (2019), 251–260.
- L. Szalay, V. Ziegler, *On an S-unit variant of Diophantine m-tuples*,
  Publ. Math. Debrecen **83** (2013), 97–121.
- E. B. Füredi, *Erdős–Turán-tétel és általánosításai*, BSc thesis, ELTE, 2024
  (supervisor K. Gyarmati). Computes the equivalent quantity f(n) for n = 5..8.
- T. F. Bloom, *Erdős Problem #126*, https://www.erdosproblems.com/126
