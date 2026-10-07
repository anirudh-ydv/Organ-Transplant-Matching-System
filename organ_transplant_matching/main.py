"""
Smart Organ Transplant Matching System  -  Anirudh Yadav, DSA-II (CCSE0301)

Run:  python main.py          -> interactive menu
      python main.py demo     -> runs every module once, no typing needed
"""
import sys
import dp_organ_matching as dp
from avl_tree import AVLTree
from max_heap import MaxHeap
from compat_graph import build_donor_graph, build_exchange_graph

TRAVEL = dp.floyd_warshall(dp.CITIES, dp.LINKS)
BYID = {r[0]: r for r in dp.RECIPIENTS}


def load_waiting_list():
    t = AVLTree()
    for r in dp.RECIPIENTS:
        t.insert(r[0], r)
    return t


def fmt(r):
    return (f"{r[0]}  blood={r[1]:<2} organ={r[2]:<6} urgency={r[3]:>2} "
            f"wait={r[4]:>4}d  city={r[6]}")


def hr(title):
    print("\n" + "=" * 70 + f"\n {title}\n" + "=" * 70)


# ------------------------------------------------------------ features
def show_list(tree):
    hr("1. Waiting list (AVL tree, inorder = sorted by ID)")
    for _, r in tree.inorder():
        print(" ", fmt(r))
    print(f"  records={tree.size}  tree height={tree.height()}  rotations={tree.rotations}  "
          f"balanced={tree.is_balanced()}")


def search(tree, rid):
    hr(f"2. AVL search for {rid}")
    r = tree.search(rid)
    print("  ", fmt(r) if r else "not found")


def add_recipient(tree, rec):
    tree.insert(rec[0], rec)
    BYID[rec[0]] = rec
    dp.RECIPIENTS.append(rec)


def match(donor_blood, organ, city, k=3):
    hr(f"3. Match: {organ} donor, blood {donor_blood}, in {city}")
    ranked = dp.rank(donor_blood, organ, city, TRAVEL)
    if not ranked:
        print("  No compatible recipient (ABO / organ type / viability time gates).")
        return
    heap = MaxHeap()
    for score, rid in ranked:
        heap.push(score, rid)
    print(f"  Gates: ABO rule, same organ, transport <= {dp.VIABLE_H[organ]} h.  "
          f"{len(heap)} recipient(s) pass.")
    print(f"  Top-{k} (Max Heap):")
    for pos, (score, rid) in enumerate(heap.top_k(k), 1):
        L = dp.lcs(dp.DONOR_HLA.split(), BYID[rid][5].split())[0]
        print(f"   {pos}. {rid}  score={score:5.1f}  HLA LCS={L}/6  "
              f"travel={TRAVEL[(city, BYID[rid][6])]} h")


def graph_view(donor_blood, organ):
    hr(f"4. Compatibility graph + BFS / DFS  (donor {donor_blood}, {organ})")
    g = build_donor_graph(donor_blood, dp.RECIPIENTS, organ)
    start = f"Donor({donor_blood})"
    print("  Adjacency list:")
    for u, vs in g.adj.items():
        if vs:
            print(f"    {u} -> {', '.join(vs)}")
    print("  BFS (node, level):", g.bfs(start))
    print("  DFS order        :", g.dfs(start))


def exchange():
    hr("5. Paired exchange (DFS cycle search)")
    g = build_exchange_graph()
    print("  Edges (donor of X can give to recipient of Y):")
    for u, vs in g.adj.items():
        print(f"    {u} -> {', '.join(vs)}")
    print("  Exchange cycles (2-3 pairs):")
    for c in g.cycles():
        print("    " + " -> ".join(c + (c[0],)))


def schedule(hours=18):
    hr(f"6. 0/1 Knapsack - choose transplants within {hours} operating hours")
    offers = []
    for organ, blood, city in [("Kidney", "O", "Delhi"), ("Liver", "A", "Delhi"),
                               ("Heart", "O", "Delhi"), ("Kidney", "B", "Noida"),
                               ("Liver", "O", "Noida"), ("Kidney", "AB", "Lucknow")]:
        top = dp.rank(blood, organ, city, TRAVEL)
        if top:
            offers.append((f"{organ}->{top[0][1]}", round(top[0][0]), dp.SURGERY_H[organ]))
    print("  Offers (best match, value, hours):")
    for o in offers:
        print(f"    {o[0]:<14} value={o[1]:>3}  hours={o[2]}")
    vals, wts = [o[1] for o in offers], [o[2] for o in offers]
    best, ch = dp.knapsack_01(vals, wts, hours)
    print(f"  DP result : {[offers[i][0] for i in ch]}  value={best}  hours={sum(wts[i] for i in ch)}")
    print(f"  Greedy    : value={dp.knapsack_greedy(vals, wts, hours)}")


def allocation():
    hr("7. Resource Allocation - 5 surgical teams, 3 hospitals")
    profit = [[0, 20, 38, 50, 58, 62], [0, 15, 30, 46, 52, 55], [0, 25, 40, 48, 52, 54]]
    best, a = dp.resource_allocation(profit, 5)
    for i, k in enumerate(a, 1):
        print(f"    Hospital {i}: {k} team(s)")
    print(f"  Total profit = {best}")


def lcs_demo():
    hr("8. LCS - HLA similarity of donor vs recipients")
    print("  Donor HLA:", dp.DONOR_HLA)
    for r in dp.RECIPIENTS[:5]:
        L, seq = dp.lcs(dp.DONOR_HLA.split(), r[5].split())
        print(f"    {r[0]}: LCS={L}/6  common={seq}")


def travel_table():
    hr("9. Floyd-Warshall - travel time between cities (hours)")
    print("  " + " " * 11 + "".join(f"{c[:6]:>8}" for c in dp.CITIES))
    for a in dp.CITIES:
        print(f"  {a:<11}" + "".join(f"{TRAVEL[(a, b)]:>8}" for b in dp.CITIES))


# ------------------------------------------------------------ modes
def demo():
    t = load_waiting_list()
    show_list(t); search(t, "R04")
    match("O", "Kidney", "Delhi"); match("A", "Liver", "Delhi"); match("O", "Heart", "Delhi")
    graph_view("O", "Kidney"); exchange()
    schedule(); allocation(); lcs_demo(); travel_table()
    print("\nDemo finished. Tests: python test_phase1_structures.py  |  python dp_organ_matching.py test")


MENU = """
 ---------------- ORGAN TRANSPLANT MATCHING SYSTEM ----------------
  1  Show waiting list (AVL tree)        6  Schedule transplants (0/1 Knapsack)
  2  Search recipient by ID (AVL)        7  Allocate surgical teams (Resource Alloc.)
  3  Match an organ offer (Top-K Heap)   8  HLA similarity (LCS)
  4  Compatibility graph (BFS / DFS)     9  City travel times (Floyd-Warshall)
  5  Paired exchange cycles (DFS)        A  Add a new recipient
  0  Exit
 ------------------------------------------------------------------"""


def ask(prompt, options=None, default=None):
    while True:
        v = input(prompt).strip()
        if not v and default is not None:
            return default
        if options is None or v in options:
            return v
        print("  Please choose from:", ", ".join(options))


def menu():
    t = load_waiting_list()
    while True:
        print(MENU)
        c = input("Choice: ").strip().upper()
        if c == "0":
            print("Goodbye."); break
        elif c == "1": show_list(t)
        elif c == "2": search(t, input("Recipient ID (e.g. R04): ").strip().upper())
        elif c == "3":
            organ = ask("Organ (Kidney/Liver/Heart): ", ["Kidney", "Liver", "Heart"])
            blood = ask("Donor blood group (O/A/B/AB): ", ["O", "A", "B", "AB"])
            city = ask(f"Donor city {dp.CITIES}: ", dp.CITIES)
            match(blood, organ, city, int(ask("How many (Top-K) [3]: ", default="3")))
        elif c == "4":
            graph_view(ask("Donor blood group (O/A/B/AB): ", ["O", "A", "B", "AB"]),
                       ask("Organ (Kidney/Liver/Heart): ", ["Kidney", "Liver", "Heart"]))
        elif c == "5": exchange()
        elif c == "6": schedule(int(ask("Operating hours available [18]: ", default="18")))
        elif c == "7": allocation()
        elif c == "8": lcs_demo()
        elif c == "9": travel_table()
        elif c == "A":
            rid = f"R{len(dp.RECIPIENTS) + 1:02d}"
            blood = ask("Blood group (O/A/B/AB): ", ["O", "A", "B", "AB"])
            organ = ask("Organ (Kidney/Liver/Heart): ", ["Kidney", "Liver", "Heart"])
            urg = int(ask("Urgency 1-10: ", [str(i) for i in range(1, 11)]))
            wait = int(ask("Waiting days: "))
            hla = ask("HLA sequence (6 antigens, e.g. A2 A24 B7 B35 DR4 DR15): ")
            city = ask(f"City {dp.CITIES}: ", dp.CITIES)
            add_recipient(t, (rid, blood, organ, urg, wait, hla, city))
            print(f"  Added {rid}. AVL height now {t.height()}, rotations {t.rotations}.")
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    try:
        demo() if len(sys.argv) > 1 and sys.argv[1] == "demo" else menu()
    except (EOFError, KeyboardInterrupt):
        print("\nExited.")
