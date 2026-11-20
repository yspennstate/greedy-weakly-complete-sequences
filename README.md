# Greedy weakly complete sequences with initial terms n and n+d

Yitzchak Shmalo

Fix integers 1 <= d < n. The greedy sequence with a_1 = n, a_2 = n + d takes as each later term the least integer
larger than the previous one that is not a sum of distinct earlier terms. Knapp and Paul conjectured an explicit
formula for this sequence (Conjecture B of their 2012 paper in Integers). They proved the case d = 1, and Fox and
Knapp (J. Integer Seq. 2013) proved 2 <= d <= n - 8. The paper proves the remaining cases n - 7 <= d <= n - 1.

## Files

- `main.tex`, `main.pdf`: the paper.
- `check_greedy_sequences.py`: the computation used in the proof and the further checks described in its final
  remark. Python 3, standard library only.

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
```

Part A checks the inclusion (4) of the paper for all 1 <= d < n <= 31 and for n - 7 <= d <= n - 1 with
32 <= n <= 80; the proof needs it only for n <= 19. Part B consists of two altered conditions that must fail, and do.
Part C computes the greedy sequence directly and compares it with the formula. Part D starts one block from the set
R_T for many values of T and compares the terms and the new set of sums with Lemma 2.3.
