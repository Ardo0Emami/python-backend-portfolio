from typing import Generic, TypeVar, Callable

T = TypeVar("T")


class BaseSortedList(Generic[T]):

    def __init__(
            self,
            compare_func: Callable[[T, T], int],
            reverse: bool = False
            ) -> None:
        self._Items: list[T] = []
        self._compare = compare_func
        self._reverse = reverse

    def add(self, item: T) -> None:
        # for i in range(len(self._Items)):
        for i, currentItem in enumerate(self._Items):
            if self._compare(item, currentItem) < 0:
                self._Items.insert(i, item)
                return
        self._Items.append(item)

    def __repr__(self) -> str:
        return f"BaseSortedList({self._Items!r})"

    def __iter__(self):
        return iter(self._Items)

    def __len__(self) -> int:
        return len(self._Items)
