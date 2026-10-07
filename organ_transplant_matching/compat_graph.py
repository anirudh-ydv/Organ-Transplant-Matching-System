"""Compatibility graph (Phase 1: Graphs) - adjacency list, BFS, DFS, paired-exchange cycles.

Graph 1: Donor -> Blood-group nodes -> Recipients  (BFS finds every compatible recipient)
Graph 2: patient-donor PAIRS; edge Pi -> Pj if Pi's donor can donate to Pj's recipient.
         DFS finds 2- and 3-way exchange cycles."""
from collections import deque
from dp_organ_matching import ABO


class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, [])

    def bfs(self, start):
        seen, order, q = {start: 0}, [], deque([start])
        while q:
            u = q.popleft(); order.append((u, seen[u]))
            for v in self.adj.get(u, []):
                if v not in seen:
                    seen[v] = seen[u] + 1; q.append(v)
        return order                                   # (node, level)

    def dfs(self, start):
        seen, order = set(), []
        def go(u):
            seen.add(u); order.append(u)
            for v in self.adj.get(u, []):
                if v not in seen:
                    go(v)
        go(start)
        return order

    def cycles(self, max_len=3):
        """simple directed cycles of length 2..max_len (each reported once)"""
        found = set()
        def go(start, u, path):
            for v in self.adj.get(u, []):
                if v == start and len(path) >= 2:
                    k = path.index(min(path))
                    found.add(tuple(path[k:] + path[:k]))
                elif v not in path and len(path) < max_len and v > start:
                    go(start, v, path + [v])
        for s in sorted(self.adj):
            go(s, s, [s])
        return sorted(found)


def build_donor_graph(donor_blood, recipients, organ):
    g = Graph()
    donor = f"Donor({donor_blood})"
    for grp in sorted(ABO[donor_blood]):
        g.add_edge(donor, f"Group {grp}")
    for r in recipients:
        if r[2] == organ and r[1] in ABO[donor_blood]:
            g.add_edge(f"Group {r[1]}", r[0])
    return g


# patient-donor pairs: (pair id, recipient blood, willing-donor blood)
PAIRS = [("P1", "A", "B"), ("P2", "B", "A"), ("P3", "O", "A"),
         ("P4", "A", "AB"), ("P5", "AB", "O")]


def build_exchange_graph(pairs=PAIRS):
    g = Graph()
    for pi, _, d in pairs:
        g.adj.setdefault(pi, [])
        for pj, rb, _ in pairs:
            if pi != pj and rb in ABO[d]:
                g.add_edge(pi, pj)
    return g
