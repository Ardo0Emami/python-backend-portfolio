from typing import Generic, TypeVar
from collections import deque

T = TypeVar("T")


class Queue(Generic[T]):
    """
    FIFO Queue.

    Time complexity:
    - enqueue: O(1)
    - dequeue: O(1)
    - peek: O(1)
    """

    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({list(self._items)!r})"
