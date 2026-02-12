from __future__ import annotations

from typing import Callable, Generic, Iterator, TypeVar

T = TypeVar("T")
CompareFunc = Callable[[T, T], int]


class BaseSortedList(Generic[T]):
    """
    compare(a, b) should return:
      < 0  if a < b
      = 0  if a == b
      > 0  if a > b

    Complexity:
    - find insertion point: O(log n) comparisons (binary search)
    - insert into list: O(n) (shifts elements)
    - overall add: O(n)
    """

    def __init__(self, compare_func: CompareFunc, reverse: bool = False) -> None:
        self._items: list[T] = []
        self._compare: CompareFunc = compare_func
        self._reverse = reverse

    def _cmp(self, a: T, b: T) -> int:
        r = self._compare(a, b)
        return -r if self._reverse else r

    def add(self, item: T) -> None:
        # insert after existing equals.
        lo, hi = 0, len(self._items)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._cmp(item, self._items[mid]) < 0:
                hi = mid
            else:
                lo = mid + 1
        self._items.insert(lo, item)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"BaseSortedList({self._items!r}, reverse={self._reverse})"