# Checks for "Greedy weakly complete sequences with initial terms n and n+d".
#   A. inclusion (eq:gap) for 0<=r<K, all 1<=d<n<=31 and n-7<=d<=n-1 for 32<=n<=80; Q_r by the size-indexed update over W.
#   B. controls that must fail: the hole of W at d instead of d-1; the translate d-1 dropped from (eq:gap).
#   C. the greedy sequence computed directly (bit sets) against n, [C,C+n-1], M_i+W for three blocks, 1<=d<n<=NMAX.
#   D. one block started from R_T for 400 consecutive values of T, n<=12, terms and the new set of sums compared.
#   E. the left side of (eq:gap) is empty for 2<=r<=K-3 when d<=n-6, and non-empty at r=2 when 4<=d, n-5<=d<=n-2 (10<=n<=150).
# Usage: python check_greedy_sequences.py [NMAX]   (default 20; a few seconds)
import sys
from math import comb

def qsets(W):
    K = len(W)
    Q = [0] * (K + 1)
    Q[0] = 1
    for w in W:
        for j in range(K, 0, -1):
            Q[j] |= Q[j - 1] << w
    return Q

def lo(x):
    return (x & -x).bit_length() - 1

def check1(n, d, hole=None, drop_dm1=False):
    C = n + d
    h0 = d - 1 if hole is None else hole
    W = [w for w in range(n) if w != h0]
    Q = qsets(W)
    K = len(W)
    nonempty = fails = 0
    for r in range(K):
        hr = Q[r].bit_length() - 1
        l1 = lo(Q[r + 1])
        a, b = hr, l1 + C - 1
        if a > b:
            continue
        nonempty += 1
        cover = (Q[r] << (C - 1)) | (Q[r + 1]) | (Q[r + 1] << n)
        if not drop_dm1:
            cover |= Q[r] << (d - 1)
        need = ((1 << (b - a + 1)) - 1) << a
        if cover & need != need:
            fails += 1
    return K, nonempty, fails

def greedy_blocks(n, d, blocks):
    C = n + d
    seq = [n] + list(range(C, C + n))
    bits = 1
    for t in seq:
        bits |= bits << t
    W = [w for w in range(n) if w != d - 1]
    M = n + n * C + comb(n, 2) - C + 1
    for _ in range(blocks):
        want = [M + w for w in W]
        got = []
        x = seq[-1] + 1
        for _k in range(len(W)):
            x = x + lo(~(bits >> x))
            got.append(x)
            bits |= bits << x
            x += 1
        if got != want:
            return False, M
        seq += got
        M = n * M + comb(n, 2) - (d - 1)
    # the term after the last block must be the next M (first entry of the next block)
    x = seq[-1] + 1
    x = x + lo(~(bits >> x))
    return x == M + W[0], M

def state_bits(n, d, T):
    C = n + d
    b = (1 << (T - 2 * C + 1)) - 1
    b <<= C
    for v in (0, n, T, T - n):
        b |= 1 << v
    return b

def one_block(n, d, T, last):
    C = n + d
    bits = state_bits(n, d, T)
    W = [w for w in range(n) if w != d - 1]
    M = T - C + 1
    x = last + 1
    got = []
    for _k in range(len(W)):
        x = x + lo(~(bits >> x))
        got.append(x)
        bits |= bits << x
        x += 1
    T2 = T + sum(got)
    ok_terms = got == [M + w for w in W]
    ok_state = bits == state_bits(n, d, T2)
    return ok_terms, ok_state


if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    pairs = incl = ne = bad = 0
    for n in range(2, 81):
        for d in (range(1, n) if n <= 31 else range(n - 7, n)):
            K, a, f = check1(n, d)
            pairs += 1; incl += K; ne += a; bad += f
            if f:
                print("A  FAILS n=%d d=%d" % (n, d))
    print("A  pairs", pairs, "inclusions", incl, "non-empty", ne, "failures", bad)
    for name, kw in (("hole at d", "hole"), ("translate d-1 dropped", "drop")):
        fp = tot = 0
        for n in range(3, 32):
            for d in range(1, n - 1) if kw == "hole" else range(2, n):
                K, a, f = check1(n, d, hole=d) if kw == "hole" else check1(n, d, drop_dm1=True)
                tot += 1; fp += (f > 0)
        print("B  control (%s): pairs failing %d of %d" % (name, fp, tot))
    gb = gp = 0
    for n in range(2, NMAX + 1):
        for d in range(1, n):
            ok, _ = greedy_blocks(n, d, 3)
            gp += 1; gb += (not ok)
            if not ok:
                print("C  MISMATCH n=%d d=%d" % (n, d))
    print("C  greedy sequence, three blocks, n<=%d:" % NMAX, gp, "pairs, failures", gb)
    tot = bt = bs = 0
    for n in range(2, 13):
        for d in range(1, n):
            C = n + d
            for T in range(2 * C + 2 * n, 2 * C + 2 * n + 400):
                ot, os_ = one_block(n, d, T, C + n - 1)
                tot += 1; bt += (not ot); bs += (not os_)
    print("D  one block from R_T, n<=12, 400 values of T each:", tot, "cases, wrong terms", bt, "wrong sets", bs)
    e_bad = e_tot = f_bad = f_tot = 0
    for n in range(10, 151):
        for d in range(1, n):
            W = [w for w in range(n) if w != d - 1]
            Q = qsets(W)
            K = len(W)
            C = n + d
            gap = [Q[r].bit_length() - 1 <= lo(Q[r + 1]) + C - 1 for r in range(K)]
            if d <= n - 6:
                e_tot += 1
                e_bad += any(gap[r] for r in range(2, K - 2))
            if 4 <= d and n - 5 <= d <= n - 2:
                f_tot += 1
                f_bad += (not gap[2])
    print("E  left side of (eq:gap) empty for 2<=r<=K-3, d<=n-6, 10<=n<=150:", e_tot, "pairs, exceptions", e_bad)
    print("E  left side non-empty at r=2, 4<=d, n-5<=d<=n-2, 10<=n<=150:", f_tot, "pairs, exceptions", f_bad)
