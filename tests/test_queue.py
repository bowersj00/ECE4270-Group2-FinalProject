from dram.queue import BoundedQueue


def test_queue_depth():
    q = BoundedQueue(max_depth=1)
    assert q.enqueue("a") is True
    assert q.enqueue("b") is False
    assert len(q) == 1
