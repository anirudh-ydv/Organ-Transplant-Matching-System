"""AVL Tree - self-balancing search tree for the recipient waiting list (Phase 1: Trees).
Key = recipient ID. Supports insert, search, delete, inorder traversal, height, rotation count."""


class Node:
    def __init__(self, key, data):
        self.key, self.data = key, data
        self.left = self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.rotations = 0

    # ---- helpers
    @staticmethod
    def _h(n):
        return n.height if n else 0

    def _update(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _balance(self, n):
        return self._h(n.left) - self._h(n.right) if n else 0

    def _rot_right(self, y):
        x = y.left
        y.left, x.right = x.right, y
        self._update(y); self._update(x)
        self.rotations += 1
        return x

    def _rot_left(self, x):
        y = x.right
        x.right, y.left = y.left, x
        self._update(x); self._update(y)
        self.rotations += 1
        return y

    def _rebalance(self, n):
        self._update(n)
        b = self._balance(n)
        if b > 1:                                   # left heavy
            if self._balance(n.left) < 0:           # LR
                n.left = self._rot_left(n.left)
            return self._rot_right(n)               # LL
        if b < -1:                                  # right heavy
            if self._balance(n.right) > 0:          # RL
                n.right = self._rot_right(n.right)
            return self._rot_left(n)                # RR
        return n

    # ---- operations
    def insert(self, key, data=None):
        def ins(n):
            if not n:
                self.size += 1
                return Node(key, data)
            if key < n.key:
                n.left = ins(n.left)
            elif key > n.key:
                n.right = ins(n.right)
            else:
                n.data = data                       # update existing record
                return n
            return self._rebalance(n)
        self.root = ins(self.root)

    def search(self, key):
        n = self.root
        while n:
            if key == n.key:
                return n.data
            n = n.left if key < n.key else n.right
        return None

    def delete(self, key):
        def dele(n, k):
            if not n:
                return None, False
            if k < n.key:
                n.left, ok = dele(n.left, k)
            elif k > n.key:
                n.right, ok = dele(n.right, k)
            else:
                if not n.left:
                    return n.right, True
                if not n.right:
                    return n.left, True
                s = n.right                          # inorder successor
                while s.left:
                    s = s.left
                n.key, n.data = s.key, s.data
                n.right, ok = dele(n.right, s.key)
            return self._rebalance(n), ok
        self.root, removed = dele(self.root, key)
        if removed:
            self.size -= 1
        return removed

    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append((n.key, n.data)); go(n.right)
        go(self.root)
        return out

    def height(self):
        return self._h(self.root)

    def is_balanced(self):
        def ok(n):
            return True if not n else abs(self._balance(n)) <= 1 and ok(n.left) and ok(n.right)
        return ok(self.root)
