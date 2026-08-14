import sys, subprocess, itertools, time
from sympy import prime, primerange
K=int(sys.argv[1]); X=sys.argv[2]; EXTRA=int(sys.argv[3]) if len(sys.argv)>3 else 5
S0=[prime(i) for i in range(1,K+1)]
extra=[prime(i) for i in range(K+1,K+1+EXTRA)]
cands=[tuple(S0)]
# swap one element (not 2) for one of the next EXTRA primes
for i in range(1,K):
    for e in extra:
        s=S0[:]; s[i]=e; cands.append(tuple(sorted(s)))
# drop one, add one (same as above) + swap two
#for (i,j) in itertools.combinations(range(1,K),2):
#    for (e,f) in itertools.combinations(extra,2):
#        pass
cands=list(dict.fromkeys(cands))
best=(0,None,None); t0=time.time()
for S in cands:
    try:
        out=subprocess.run(["./gk",X]+[str(p) for p in S],capture_output=True,text=True,timeout=90).stdout
        n=int(out.split("|A|=")[1].split()[0]); A=out.split("A=")[1].split()[0]
    except Exception: continue
    if n>best[0]:
        best=(n,S,A)
        print(f"   new best {n}  S={list(S)}",flush=True)
print(f"k={K}: E1 >= {best[0]}   ({len(cands)} sets, {time.time()-t0:.0f}s)")
print(f"   S={list(best[1])}")
print(f"   A={best[2]}")
