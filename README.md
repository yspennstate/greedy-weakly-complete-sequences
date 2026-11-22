# Greedy weakly complete sequences with initial terms n and n+d

Yitzchak Shmalo

Zenodo: https://doi.org/10.5281/zenodo.24433227 (all versions)

Fix integers 1 <= d < n. The greedy sequence with x_1 = n, x_2 = n + d takes as each later term the least integer
larger than the previous one that is not a sum of distinct earlier terms. Paul conjectured an explicit
formula for this sequence (Conjecture B of Knapp and Paul, Integers 2012). Knapp and Paul proved the case d = 1, and Fox and
Knapp (J. Integer Seq. 2013) proved 2 <= d <= n - 8. The paper proves the remaining cases n - 7 <= d <= n - 1.

## Files

- `main.tex`, `main.pdf`: the paper.
- `check_greedy_sequences.py`: the checks listed in the Data and code availability section of the paper. Python 3, standard library only.

```
python check_greedy_sequences.py        # n <= 20 for the direct greedy check; runs in a few seconds
```

Expected output:

```
A  pairs 808 inclusions 28320 non-empty 3999 failures 0
B  control (hole at d): pairs failing 435 of 435
B  control (translate d-1 dropped): pairs failing 435 of 435
C  greedy sequence, three blocks, n<=20: 190 pairs, failures 0
D  one block from R_T, n<=12, 400 values of T each: 26400 cases, wrong terms 0 wrong sets 0
E  left side of (eq:gap) empty for 2<=r<=K-3, d<=n-6, 10<=n<=150: 10434 pairs, exceptions 0
E  left side non-empty at r=2, 4<=d, n-5<=d<=n-1, 10<=n<=150: 705 pairs, exceptions 0
F  Lemma 3.1 (a) and (b), 2<=d<n<=60: 1711 pairs, failures (a) 0 (b) 0
```

Part A checks the inclusion (3) of the paper for all 1 <= d < n <= 31 and for n - 7 <= d <= n - 1 with
32 <= n <= 80. Part B consists of two altered conditions that must fail, and do.
Part C computes the greedy sequence directly and compares it with the formula. Part D starts one block from the set
R_T for many values of T and compares the terms and the new set of sums with Lemma 2.3. Part E checks the two statements of Remark 3.2 on the left side of (3) for 10 <= n <= 150. Part F checks parts (a)
and (b) of Lemma 3.1, which give (3) for r <= K-2, for 2 <= d < n <= 60. The proof itself does not depend on a computation.
