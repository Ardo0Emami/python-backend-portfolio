import unittest
from queue import Queue


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue[int]()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertTrue(q.is_empty())

    def test_peek(self):
        q = Queue[str]()
        q.enqueue("ard")
        self.assertEqual(q.peek(), "ard")
        self.assertFalse(q.is_empty())

    def test_dequeue_empty_raises(self):
        q = Queue[int]()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek_empty_raises(self):
        q = Queue[int]()
        with self.assertRaises(IndexError):
            q.peek()


if __name__ == "__main__":
    unittest.main()
