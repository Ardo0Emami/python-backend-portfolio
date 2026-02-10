from typing import Generic, TypeVar

T = TypeVar("T")


# Queue class
class Queue(Generic[T]):
    def __init__(self) -> None:
        self._Items: list[T] = []

    def enqueue(self, item: T) -> None:
        self._Items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._Items.pop(0)

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty queue")
        return self._Items[0]

    def is_empty(self) -> bool:
        return len(self._Items) == 0

    def __len__(self) -> int:
        return len(self._Items)

    def __repr__(self) -> str:
        return f"Queue({self._Items!r})"
