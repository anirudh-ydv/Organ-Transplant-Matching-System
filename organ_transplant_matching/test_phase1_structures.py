"""Tests for the Phase 1 structures: AVL tree, Max Heap, compatibility graph."""
import random
import unittest
from avl_tree import AVLTree
from max_heap import MaxHeap
from compat_graph import Graph, build_donor_graph, build_exchange_graph
from dp_organ_matching import RECIPIENTS


class TestAVL(unittest.TestCase):
    def test_insert_search(self):
        t = AVLTree()
        for k in ["R05", "R02", "R09", "R01"]:
            t.insert(k, k.lower())
        self.assertEqual(t.search("R09"), "r09")
        self.assertIsNone(t.search("R99"))

    def test_inorder_sorted(self):
        t = AVLTree()
        keys = [f"R{i:02d}" for i in range(1, 11)]
        random.Random(3).shuffle(keys)
        for k in keys:
            t.insert(k)
        self.assertEqual([k for k, _ in t.inorder()], sorted(keys))

    def test_sorted_input_stays_balanced(self):
        t = AVLTree()
        for i in range(1, 128):
            t.insert(i)
        self.assertTrue(t.is_balanced())
        self.assertLessEqual(t.height(), 8)          # a plain BST would be 127 tall

    def test_rotations_happen(self):
        t = AVLTree()
        for i in (1, 2, 3):
            t.insert(i)                               # RR case
        self.assertEqual(t.root.key, 2)
        self.assertEqual(t.rotations, 1)

    def test_lr_case(self):
        t = AVLTree()
        for i in (3, 1, 2):
            t.insert(i)
        self.assertEqual(t.root.key, 2)

    def test_delete(self):
        t = AVLTree()
        for i in range(1, 21):
            t.insert(i)
        self.assertTrue(t.delete(10))
        self.assertFalse(t.delete(10))
        self.assertIsNone(t.search(10))
        self.assertEqual(t.size, 19)
        self.assertTrue(t.is_balanced())

    def test_duplicate_updates(self):
        t = AVLTree(); t.insert("A", 1); t.insert("A", 2)
        self.assertEqual(t.size, 1)
        self.assertEqual(t.search("A"), 2)


class TestHeap(unittest.TestCase):
    def test_pop_order(self):
        h = MaxHeap()
        for s in [5, 1, 9, 3, 7]:
            h.push(s, str(s))
        self.assertEqual([h.pop()[0] for _ in range(5)], [9, 7, 5, 3, 1])

    def test_top_k_non_destructive(self):
        h = MaxHeap()
        for s in [5, 1, 9, 3, 7]:
            h.push(s, str(s))
        self.assertEqual([x[0] for x in h.top_k(3)], [9, 7, 5])
        self.assertEqual(len(h), 5)

    def test_empty(self):
        self.assertIsNone(MaxHeap().pop())

    def test_random_matches_sorted(self):
        rnd = random.Random(7); vals = [rnd.randint(0, 999) for _ in range(200)]
        h = MaxHeap()
        for v in vals:
            h.push(v, v)
        self.assertEqual([h.pop()[0] for _ in vals], sorted(vals, reverse=True))


class TestGraph(unittest.TestCase):
    def test_bfs_levels(self):
        g = Graph()
        for u, v in [("S", "A"), ("S", "B"), ("A", "D"), ("B", "D")]:
            g.add_edge(u, v)
        self.assertEqual(g.bfs("S"), [("S", 0), ("A", 1), ("B", 1), ("D", 2)])

    def test_dfs_order(self):
        g = Graph()
        for u, v in [("S", "A"), ("A", "D"), ("S", "B")]:
            g.add_edge(u, v)
        self.assertEqual(g.dfs("S"), ["S", "A", "D", "B"])

    def test_donor_graph_o_kidney(self):
        g = build_donor_graph("O", RECIPIENTS, "Kidney")
        recs = {n for n, lvl in g.bfs("Donor(O)") if n.startswith("R")}
        self.assertEqual(recs, {"R01", "R02", "R03", "R04", "R05"})

    def test_donor_graph_a_kidney(self):
        g = build_donor_graph("A", RECIPIENTS, "Kidney")
        recs = {n for n, lvl in g.bfs("Donor(A)") if n.startswith("R")}
        self.assertEqual(recs, {"R02", "R05"})        # A and AB recipients only

    def test_exchange_pair(self):
        self.assertIn(("P1", "P2"), build_exchange_graph().cycles())

    def test_cycles_valid(self):
        g = build_exchange_graph()
        for c in g.cycles():
            for i, u in enumerate(c):
                self.assertIn(c[(i + 1) % len(c)], g.adj[u])


if __name__ == "__main__":
    unittest.main(verbosity=1)
