# Smart Organ Transplant Matching System
DSA-II (CCSE0301) PBL project - Anirudh Yadav - SDG 3 (Good Health and Well-Being)

A console prototype that matches a donor organ to the best recipient using data structures
and algorithms from Unit 1 (Trees), Unit 2 (Graphs) and Unit 3 (Dynamic Programming).
All data is synthetic (real patient data is confidential). Needs only Python 3.8+ (no installs).

## How to run
    python main.py            # interactive menu
    python main.py demo       # runs every module once, no typing needed
    python run_all_tests.py   # all 35 unit tests
    python dp_organ_matching.py        # Phase 2 demo + benchmark (DP vs brute force)
    python dp_organ_matching.py test   # the 18 Phase 2 tests only

## Files
| File | What it does | Report |
|---|---|---|
| avl_tree.py | AVL tree waiting list: insert, search, delete, rotations | Phase 1 (Trees) |
| max_heap.py | Max Heap, non-destructive Top-K ranking | Phase 1 (Heaps) |
| compat_graph.py | Adjacency-list graph, BFS, DFS, paired-exchange cycles | Phase 1 (Graphs) |
| dp_organ_matching.py | Floyd-Warshall, LCS, MatchScore, 0/1 Knapsack, Resource Allocation | Phase 2 (Unit 3) |
| main.py | Menu that connects all modules | Both |
| test_phase1_structures.py | 17 tests for AVL, heap, graph | Phase 1 |
| run_all_tests.py | Runs all 35 tests | Both |

## How a match works
1. Hard gates: same organ, ABO rule, transport time within the organ's viability limit (else score 0).
2. HLA similarity = LCS length / 6 (Unit 3).
3. MatchScore = 100 x (0.40 x urgency/10 + 0.30 x HLA + 0.30 x waiting/1500). Weights are design assumptions.
4. Max Heap returns the Top-K recipients.
5. 0/1 Knapsack picks which transplants fit the operating-theatre hours.
This is a learning prototype, not a clinical tool.
