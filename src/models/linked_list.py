import math

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None 
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0
    
    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last = self.head.prev
            last.next = new_node
            new_node.prev = last
            new_node.next = self.head
            self.head.prev = new_node
        self._size += 1
        return new_node

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

    @staticmethod
    def build_ticks(n=60):
        lst = CircularDoublyLinkedList()
        for i in range(n):
            deg = i * (360 / n)
            rad = math.radians(deg)
            lst.insert_at_end({'index': i, 'deg': deg, 'rad': rad})
        return lst