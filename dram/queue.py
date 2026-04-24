"""Bounded request queue."""

class BoundedQueue:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self._items = []

    def enqueue(self, req) -> bool:
        if len(self._items) >= self.max_depth:
            return False
        self._items.append(req)
        return True

    def remove(self, req):
        self._items.remove(req)

    def items(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)

    def is_full(self):
        return len(self._items) >= self.max_depth
