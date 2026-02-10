import unittest
from stack import Stack, StackEmptyError


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push("A")
        s.push("B")

        self.assertEqual(s.pop(), "B")
        self.assertEqual(s.pop(), "A")
        self.assertTrue(s.is_empty())

    def test_peek(self):
        s = Stack()
        s.push("A")
        self.assertEqual("A", s.peek())
        self.assertFalse(s.is_empty())
        self.assertEqual(s.size(), 1)

    def test_empty_pop_raises(self):
        s = Stack()
        with self.assertRaises(StackEmptyError):
            s.pop()

    def test_empty_peek_raises(self):
        s = Stack()
        with self.assertRaises(StackEmptyError):
            s.peek()

    def test_int_stack(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_iteration_and_len(self):
        s = Stack[str]()
        s.push("x")
        s.push("y")
        s.push("z")
        items = [item for item in s]
        self.assertEqual(items, ["z", "y", "x"])
        self.assertEqual(len(s), 3)


if __name__ == "__main__":
    unittest.main()
