"""
Smart Organ Transplant Matching System - Phase 2 (Unit 3: Dynamic Programming)
Anirudh Yadav | DSA-II (CCSE0301)

Modules
  1. Floyd-Warshall  : all-pairs travel time between cities (DP, from the Unit 2 slides)
  2. LCS             : HLA-sequence similarity between donor and recipient
  3. MatchScore      : ABO + viability gates, then weighted score
  4. 0/1 Knapsack    : choose transplants that fit operating-theatre hours
  5. Resource Alloc. : distribute surgical teams among hospitals
All data is synthetic (real patient data is confidential).
"""
import itertools
import time
import unittest

INF = float("inf")

# ------------------------------------------------------------------ data
CITIES = ["Delhi", "Noida", "Jaipur", "Lucknow", "Chandigarh"]
# direct road links, travel time in hours (undirected)
LINKS = [("Delhi", "Noida", 1), ("Delhi", "Jaipur", 5), ("Delhi", "Chandigarh", 4),
         ("Noida", "Lucknow", 6), ("Jaipur", "Chandigarh", 7), ("Delhi", "Lucknow", 7)]

VIABLE_H = {"Kidney": 24, "Liver": 8, "Heart": 4}   # lower bound of cold-ischemia window
SURGERY_H = {"Kidney": 4, "Liver": 8, "Heart": 6}
ABO = {"O": {"O", "A", "B", "AB"}, "A": {"A", "AB"}, "B": {"B", "AB"}, "AB": {"AB"}}

# id, blood, organ, urgency(1-10), waiting days, HLA sequence, city
RECIPIENTS = [
    ("R01", "O", "Kidney", 9, 900, "A2 A24 B7 B35 DR4 DR15", "Delhi"),
    ("R02", "A", "Kidney", 6, 400, "A1 A3 B8 B44 DR3 DR7", "Noida"),
    ("R03", "O", "Kidney", 7, 1200, "A2 A3 B7 B44 DR4 DR7", "Jaipur"),
    ("R04", "B", "Kidney", 8, 700, "A1 A24 B8 B35 DR4 DR15", "Noida"),
    ("R05", "AB", "Kidney", 5, 300, "A2 A24 B7 B35 DR3 DR15", "Lucknow"),
    ("R06", "A", "Liver", 9, 200, "A1 A3 B8 B44 DR3 DR7", "Delhi"),
    ("R07", "O", "Liver", 7, 500, "A2 A24 B7 B44 DR4 DR15", "Noida"),
    ("R08", "O", "Heart", 10, 100, "A2 A24 B7 B35 DR4 DR15", "Delhi"),
    ("R09", "B", "Heart", 8, 150, "A1 A3 B8 B35 DR3 DR7", "Chandigarh"),
    ("R10", "O", "Heart", 9, 250, "A2 A3 B7 B35 DR4 DR7", "Lucknow"),
]
W_URG, W_HLA, W_WAIT = 0.40, 0.30, 0.30            # design assumption, not clinical


# ------------------------------------------------ 1. Floyd-Warshall (DP)
def floyd_warshall(cities, links):
    n = len(cities)
    idx = {c: i for i, c in enumerate(cities)}
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in links:
        d[idx[a]][idx[b]] = d[idx[b]][idx[a]] = min(d[idx[a]][idx[b]], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return {(a, b): d[idx[a]][idx[b]] for a in cities for b in cities}


# ----------------------------------------------------------- 2. LCS (DP)
def lcs(x, y):
    n, m = len(x), len(y)
    c = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c[i][j] = c[i-1][j-1] + 1 if x[i-1] == y[j-1] else max(c[i-1][j], c[i][j-1])
    out, i, j = [], n, m                              # trace back
    while i and j:
        if x[i-1] == y[j-1]:
            out.append(x[i-1]); i -= 1; j -= 1
        elif c[i-1][j] >= c[i][j-1]:
            i -= 1
        else:
            j -= 1
    return c[n][m], out[::-1]


def lcs_recursive_calls(x, y):
    """plain recursion (no memo) - counts calls, to compare with DP table size"""
    calls = 0
    def f(i, j):
        nonlocal calls
        calls += 1
        if i == 0 or j == 0:
            return 0
        if x[i-1] == y[j-1]:
            return 1 + f(i-1, j-1)
        return max(f(i-1, j), f(i, j-1))
    f(len(x), len(y))
    return calls


def hla_similarity(donor_hla, rec_hla):
    a, b = donor_hla.split(), rec_hla.split()
    length, _ = lcs(a, b)
    return length / max(len(a), len(b))


# ------------------------------------------------------- 3. MatchScore
def match_score(donor_blood, organ, donor_city, r, travel):
    rid, blood, r_organ, urg, wait, hla, city = r
    if r_organ != organ or blood not in ABO[donor_blood]:
        return 0.0                                     # hard gate: organ + ABO
    if travel[(donor_city, city)] > VIABLE_H[organ]:
        return 0.0                                     # hard gate: viability time
    return round(100 * (W_URG * urg / 10 + W_HLA * hla_similarity(DONOR_HLA, hla)
                        + W_WAIT * min(wait, 1500) / 1500), 1)


DONOR_HLA = "A2 A24 B7 B35 DR4 DR15"


def rank(donor_blood, organ, donor_city, travel, recs=RECIPIENTS):
    s = [(match_score(donor_blood, organ, donor_city, r, travel), r[0]) for r in recs]
    return sorted([x for x in s if x[0] > 0], reverse=True)


# ------------------------------------------------- 4. 0/1 Knapsack (DP)
def knapsack_01(values, weights, cap):
    n = len(values)
    c = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(cap + 1):
            c[i][w] = c[i-1][w]
            if weights[i-1] <= w:
                c[i][w] = max(c[i][w], values[i-1] + c[i-1][w - weights[i-1]])
    chosen, w = [], cap
    for i in range(n, 0, -1):                          # trace back
        if c[i][w] != c[i-1][w]:
            chosen.append(i - 1); w -= weights[i-1]
    return c[n][cap], sorted(chosen)


def knapsack_brute(values, weights, cap):
    best = 0
    for mask in itertools.product((0, 1), repeat=len(values)):
        if sum(m * w for m, w in zip(mask, weights)) <= cap:
            best = max(best, sum(m * v for m, v in zip(mask, values)))
    return best


def knapsack_greedy(values, weights, cap):            # by value/weight ratio
    tot = used = 0
    for i in sorted(range(len(values)), key=lambda k: -values[k] / weights[k]):
        if used + weights[i] <= cap:
            used += weights[i]; tot += values[i]
    return tot


# ------------------------------------- 5. Resource allocation (DP)
def resource_allocation(profit, total):
    """profit[h][k] = benefit of giving k teams to hospital h (k = 0..total)"""
    n = len(profit)
    dp = [[0] * (total + 1) for _ in range(n + 1)]
    pick = [[0] * (total + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(total + 1):
            best, bk = -1, 0
            for k in range(j + 1):
                v = profit[i-1][k] + dp[i-1][j - k]
                if v > best:
                    best, bk = v, k
            dp[i][j], pick[i][j] = best, bk
    alloc, j = [], total
    for i in range(n, 0, -1):
        alloc.append(pick[i][j]); j -= pick[i][j]
    return dp[n][total], alloc[::-1]


# ------------------------------------------------------------ tests
class Tests(unittest.TestCase):
    def setUp(self):
        self.t = floyd_warshall(CITIES, LINKS)

    def test_fw_symmetric_and_zero(self):
        for a in CITIES:
            self.assertEqual(self.t[(a, a)], 0)
            for b in CITIES:
                self.assertEqual(self.t[(a, b)], self.t[(b, a)])

    def test_fw_shortcut(self):
        self.assertEqual(self.t[("Delhi", "Lucknow")], 7)       # direct = via Noida (1+6)
        self.assertEqual(self.t[("Jaipur", "Noida")], 6)        # via Delhi 5+1

    def test_lcs_slide_example(self):
        self.assertEqual(lcs("BCDAACD", "ACDBAC")[0], 4)

    def test_lcs_stone_longest(self):
        self.assertEqual(lcs("STONE", "LONGEST")[0], 3)

    def test_lcs_empty(self):
        self.assertEqual(lcs("", "ABC"), (0, []))

    def test_lcs_matches_recursion(self):
        self.assertLess(len("ACDBAC") * len("BCDAACD"), lcs_recursive_calls("BCDAACD", "ACDBAC"))

    def test_hla_range(self):
        for r in RECIPIENTS:
            self.assertTrue(0 <= hla_similarity(DONOR_HLA, r[5]) <= 1)

    def test_hla_identical(self):
        self.assertEqual(hla_similarity(DONOR_HLA, DONOR_HLA), 1.0)

    def test_abo_gate(self):
        r = rank("A", "Kidney", "Delhi", self.t)
        self.assertTrue(all(x[1] in ("R02", "R05") for x in r))

    def test_viability_gate(self):
        ids = [x[1] for x in rank("O", "Heart", "Delhi", self.t)]
        self.assertNotIn("R10", ids)                            # Lucknow 7 h > 4 h

    def test_ranking_sorted(self):
        r = rank("O", "Kidney", "Delhi", self.t)
        self.assertEqual(r, sorted(r, reverse=True))

    def test_knapsack_slide_table(self):                        # slide 29, M = 5
        self.assertEqual(knapsack_01([3, 4, 5, 6], [2, 3, 4, 5], 5), (7, [0, 1]))

    def test_knapsack_w8(self):                                 # PYQ: W = 8
        self.assertEqual(knapsack_01([3, 4, 5, 6], [2, 3, 4, 5], 8)[0], 10)

    def test_knapsack_zero_cap(self):
        self.assertEqual(knapsack_01([5], [3], 0), (0, []))

    def test_knapsack_vs_brute(self):
        v, w = [60, 100, 120, 70, 90], [3, 4, 6, 2, 5]
        for cap in range(0, 21):
            self.assertEqual(knapsack_01(v, w, cap)[0], knapsack_brute(v, w, cap))

    def test_knapsack_traceback_valid(self):
        v, w = [60, 100, 120, 70, 90], [3, 4, 6, 2, 5]
        best, ch = knapsack_01(v, w, 12)
        self.assertEqual(best, sum(v[i] for i in ch))
        self.assertLessEqual(sum(w[i] for i in ch), 12)

    def test_resource_alloc_total(self):
        p = [[0, 2, 4, 6, 7, 8], [0, 1, 3, 5, 6, 7], [0, 3, 5, 6, 8, 9]]
        best, a = resource_allocation(p, 5)
        self.assertEqual(sum(a), 5)
        self.assertEqual(best, sum(p[i][a[i]] for i in range(3)))

    def test_resource_alloc_one_hospital(self):
        self.assertEqual(resource_allocation([[0, 4, 9]], 2), (9, [2]))


# ------------------------------------------------------------- demo
def main():
    travel = floyd_warshall(CITIES, LINKS)
    print("== Floyd-Warshall travel time from Delhi (h):",
          {c: travel[("Delhi", c)] for c in CITIES})

    print("\n== LCS: donor HLA vs recipients")
    for r in RECIPIENTS[:4]:
        L, seq = lcs(DONOR_HLA.split(), r[5].split())
        print(f"  {r[0]}: LCS={L} similarity={L/6:.2f}  common={seq}")
    a, b = "BCDAACD", "ACDBAC"
    print(f"  slide check LCS({a},{b}) = {lcs(a, b)}, recursive calls = "
          f"{lcs_recursive_calls(a, b)} vs table cells = {(len(a)+1)*(len(b)+1)}")

    print("\n== Scenarios (ABO + viability gates, then MatchScore)")
    scen = [("Kidney", "O", "Delhi"), ("Liver", "A", "Delhi"), ("Heart", "O", "Delhi")]
    for organ, blood, city in scen:
        print(f"  {organ} donor {blood}, {city}: {rank(blood, organ, city, travel)}")

    print("\n== 0/1 Knapsack: six organ offers, OR capacity 18 h")
    offers = []
    for organ, blood, city in [("Kidney", "O", "Delhi"), ("Liver", "A", "Delhi"),
                               ("Heart", "O", "Delhi"), ("Kidney", "B", "Noida"),
                               ("Liver", "O", "Noida"), ("Kidney", "AB", "Lucknow")]:
        top = rank(blood, organ, city, travel)
        if top:
            offers.append((f"{organ[0]}:{top[0][1]}", top[0][0], SURGERY_H[organ]))
    print("  offers (label, value, hours):", offers)
    vals = [round(o[1]) for o in offers]; wts = [o[2] for o in offers]
    best, ch = knapsack_01(vals, wts, 18)
    print(f"  DP -> value {best}, chosen {[offers[i][0] for i in ch]}, hours {sum(wts[i] for i in ch)}")
    print(f"  greedy(ratio) -> value {knapsack_greedy(vals, wts, 18)}")

    print("\n== Resource allocation: 5 surgical teams, 3 hospitals")
    profit = [[0, 20, 38, 50, 58, 62], [0, 15, 30, 46, 52, 55], [0, 25, 40, 48, 52, 54]]
    print("  ", resource_allocation(profit, 5))

    print("\n== Benchmark (avg of 20 runs)")
    import random
    random.seed(7)
    for n in (10, 14, 18, 20):
        v = [random.randint(20, 100) for _ in range(n)]
        w = [random.randint(2, 9) for _ in range(n)]
        cap = sum(w) // 2
        t0 = time.perf_counter()
        for _ in range(20): knapsack_01(v, w, cap)
        td = (time.perf_counter() - t0) / 20
        t0 = time.perf_counter()
        bb = knapsack_brute(v, w, cap)
        tb = time.perf_counter() - t0
        print(f"  n={n:2d} cap={cap:3d}  DP {td*1e6:9.1f} us   brute {tb*1e6:12.1f} us   same={bb == knapsack_01(v, w, cap)[0]}")

    print("\n== Greedy vs DP on 1000 random instances (n=8, seed 7)")
    random.seed(7)
    worse = 0; gap = 0
    for _ in range(1000):
        v = [random.randint(20, 100) for _ in range(8)]
        w = [random.randint(2, 9) for _ in range(8)]
        cap = sum(w) // 2
        d, g = knapsack_01(v, w, cap)[0], knapsack_greedy(v, w, cap)
        if g < d:
            worse += 1; gap += (d - g) / d
    print(f"  greedy below optimal in {worse} of 1000 cases; mean shortfall in those cases {100*gap/max(worse,1):.1f}%")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=["x"], verbosity=1)
    else:
        main()
