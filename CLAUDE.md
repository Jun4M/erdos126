# erdos126

Computational search for Erdős Problem #126. Flat layout — all files at the
repository root; do not introduce `src/`, `data/` or similar directories.

## Working rules

- After modifying `data.txt`, always run `python3 verify_data.py` and confirm
  the final line reads `30 witness sets checked -> ALL PASS`.

`verify_data.py` re-derives every witness from scratch (factoring each pairwise
value with sympy, no clique code) and checks it against the claimed cardinality,
omega and gcd. It catches transcription errors that survive a correct
computation — a stray element in a witness list is invisible by eye but shows up
immediately as `|A|` disagreeing with the claimed value.

## Build

    gcc -O2 -o gk  search_fixed_primes.c
    gcc -O2 -o e2  search_E1_E2.c
    gcc -O2 -o all search_all_primes.c

Build artifacts (`gk`, `e2`, `all`) are gitignored; remove them before
committing. `verify_data.py` and `verify_independent.py` require sympy.
