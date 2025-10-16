from src.models.linked_list import CircularDoublyLinkedList

def test_build_ticks_size():
    ticks = CircularDoublyLinkedList.build_ticks(60)
    assert ticks.size() == 60
    first = ticks.get_node_at(0)
    assert first.data['index'] == 0