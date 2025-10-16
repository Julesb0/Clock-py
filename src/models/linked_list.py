import math

class ClockTick:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def insert_at_end(self, data):
        new_tick = ClockTick(data)
        if self.head is None:
            self.head = new_tick
            new_tick.next = new_tick
            new_tick.prev = new_tick
        else:
            last = self.head.prev
            last.next = new_tick
            new_tick.prev = last
            new_tick.next = self.head
            self.head.prev = new_tick
        self._size += 1
        return new_tick

    def get_node_at(self, index):
        if self.head is None or self._size == 0:
            return None
        index = index % self._size
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

    def size(self):
        return self._size

    def to_list(self):
        out = []
        if self.head is None:
            return out
        cur = self.head
        for _ in range(self._size):
            out.append(cur.data)
            cur = cur.next
        return out

    @staticmethod
    def build_ticks(n=60):
        lst = CircularDoublyLinkedList()
        for i in range(n):
            deg = i * (360 / n)
            rad = math.radians(deg)
            lst.insert_at_end({'index': i, 'deg': deg, 'rad': rad})
        return lst