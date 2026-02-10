import unittest
from doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):
    def test_add_front_and_len(self) -> None:
        dll = DoublyLinkedList[int]()
        dll.add_front(1)
        dll.add_front(2)
        dll.add_front(3)

        self.assertEqual(len(dll), 3)

        self.assertIsNotNone(dll.head)
        assert dll.head is not None  # static type narrowing for Pylance
        self.assertEqual(dll.head.value, 3)

        self.assertIsNotNone(dll.tail)
        assert dll.tail is not None
        self.assertEqual(dll.tail.value, 1)

    def test_add_back_and_len(self) -> None:
        dll = DoublyLinkedList[int]()
        dll.add_back(1)
        dll.add_back(2)
        dll.add_back(3)

        self.assertEqual(len(dll), 3)

        self.assertIsNotNone(dll.head)
        assert dll.head is not None
        self.assertEqual(dll.head.value, 1)

        self.assertIsNotNone(dll.tail)
        assert dll.tail is not None
        self.assertEqual(dll.tail.value, 3)

    def test_find_empty_and_duplicates(self) -> None:
        dll = DoublyLinkedList[int]()
        self.assertIsNone(dll.find(123))  # empty

        dll.add_front(5)
        dll.add_front(6)
        dll.add_front(5)
        # 5,6,5 (head→tail)

        n = dll.find(5)
        self.assertIsNotNone(n)
        assert n is not None
        self.assertEqual(n.value, 5)
        # should be the head 5 (first occurrence)

    def test_remove(self) -> None:
        dll = DoublyLinkedList[int]()
        dll.add_front(5)
        dll.add_front(6)
        dll.add_front(7)
        dll.add_front(5)
        # 5, 7, 6, 5 (head→tail)
        dll.remove(5)
        dll.remove(5)
        self.assertIsNotNone(dll.head)
        self.assertIsNotNone(dll.tail)
        assert dll.head is not None
        assert dll.tail is not None
        self.assertEqual(dll.head.value, 7)
        self.assertEqual(dll.tail.value, 6)
        self.assertEqual(list(dll), [7, 6])
        self.assertEqual(len(dll), 2)

    def test_contains_iter(self) -> None:
        dll = DoublyLinkedList[int]()
        self.assertFalse(9 in dll)
        dll.add_front(4)
        dll.add_front(6)
        dll.add_front(7)
        dll.add_front(5)
        # 5, 7, 6, 4 (head→tail)
        self.assertFalse(9 in dll)
        self.assertTrue(5 in dll)
        self.assertTrue(4 in dll)
        self.assertTrue(6 in dll)
        self.assertEqual(list(dll), [5, 7, 6, 4])

    def test_repr_structure(self) -> None:
        dll = DoublyLinkedList[str]()
        dll.add_back("a")
        dll.add_back("b")
        s = repr(dll)
        self.assertTrue(s.startswith("DoublyLinkedList(["))
        self.assertIn("'a'", s)
        self.assertIn("'b'", s)
        self.assertTrue(s.endswith("])"))


if __name__ == "__main__":
    unittest.main()
