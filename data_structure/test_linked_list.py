import unittest
from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def test_add_front_and_len(self):
        lst = LinkedList[int]()
        lst.add_front(1)
        lst.add_front(2)
        lst.add_front(3)
        self.assertEqual(3, len(lst))
        self.assertEqual(list(lst), [3, 2, 1])

    def test_add_back_and_len(self):
        lst = LinkedList[int]()
        lst.add_back(1)
        lst.add_back(2)
        lst.add_back(3)
        self.assertEqual(list(lst), [1, 2, 3])
        self.assertEqual(len(lst), 3)

    def test_find(self):
        lst = LinkedList[int]()
        lst.add_back(1)
        lst.add_back(2)
        lst.add_back(3)
        self.assertEqual(lst.find(2).value, 2)
        with self.assertRaises(ValueError):
            lst.find(4)

    def test_remove_and_len(self):
        lst = LinkedList[int]()
        for x in [1, 2, 2, 3]:
            lst.add_back(x)

        with self.assertRaises(ValueError):
            lst.remove(4)

        lst.remove(2)
        self.assertEqual(list(lst), [1, 2, 3])
        self.assertEqual(len(lst), 3)

        lst.remove(1)
        self.assertEqual(list(lst), [2, 3])
        self.assertEqual(len(lst), 2)

        lst.remove(3)
        self.assertEqual(list(lst), [2])
        self.assertEqual(len(lst), 1)

        lst.remove(2)
        self.assertEqual(list(lst), [])
        self.assertEqual(len(lst), 0)

    def test_iter(self):
        lst = LinkedList[int]()
        for x in [1, 2, 3]:
            lst.add_back(x)

        # self.assertEqual([v for v in lst], [1, 2, 3])
        self.assertEqual(list(lst), [1, 2, 3])
        self.assertEqual(list(lst), [1, 2, 3])

    def test_clear_and_len(self):
        lst = LinkedList[int]()
        for x in [1, 2, 3]:
            lst.add_back(x)

        lst.clear()
        self.assertEqual(len(lst), 0)
        self.assertEqual(lst.head, None)

    def test_contains(self):
        lst = LinkedList[int]()
        for x in [1, 2, 3]:
            lst.add_back(x)
        self.assertFalse(4 in lst)
        self.assertTrue(3 in lst)

    def test_represent(self):
        lst = LinkedList[int]()
        for x in [1, 2, 3]:
            lst.add_back(x)

        self.assertEqual(lst.__repr__(), "LinkedList([1, 2, 3])")


if __name__ == "__main__":
    unittest.main()
