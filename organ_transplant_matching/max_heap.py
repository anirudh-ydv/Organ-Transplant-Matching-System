"""Max Heap - ranks recipients by MatchScore and returns Top-K (Phase 1: Heaps)."""


class MaxHeap:
    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    def push(self, score, item):
        self.a.append((score, item))
        i = len(self.a) - 1
        while i > 0:                                 # heapify-up
            p = (i - 1) // 2
            if self.a[p][0] >= self.a[i][0]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def peek(self):
        return self.a[0] if self.a else None

    def pop(self):
        if not self.a:
            return None
        top, last = self.a[0], self.a.pop()
        if self.a:
            self.a[0] = last
            i, n = 0, len(self.a)
            while True:                              # heapify-down
                l, r, m = 2 * i + 1, 2 * i + 2, i
                if l < n and self.a[l][0] > self.a[m][0]: m = l
                if r < n and self.a[r][0] > self.a[m][0]: m = r
                if m == i:
                    break
                self.a[i], self.a[m] = self.a[m], self.a[i]
                i = m
        return top

    def top_k(self, k):
        """non-destructive: works on a copy so the original heap is kept"""
        c = MaxHeap(); c.a = list(self.a)
        out = []
        for _ in range(min(k, len(c))):
            out.append(c.pop())
        return out
