import unittest
from sorted_list import BaseSortedList


class TestBaseSortedList(unittest.TestCase):

    def test_add_and_sort_int(self):
        def compare(x: int, y: int) -> int:
            return x - y

        lst = BaseSortedList(compare)
        lst.add(3)
        lst.add(1)
        lst.add(2)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_add_and_sort_str(self):
        def compare(x: str, y: str) -> int:
            return (x > y) - (x < y)

        lst = BaseSortedList(compare)
        lst.add("c")
        lst.add("a")
        lst.add("d")
        self.assertEqual(list(lst), ["a", "c", "d"])


if __name__ == "__main__":
    unittest.main()
