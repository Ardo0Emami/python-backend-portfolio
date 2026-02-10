from typing import Generic, Iterator, TypeVar, Optional

T = TypeVar("T")


class DoublyNode(Generic[T]):
    def __init__(self, value: T,
                 prev: Optional["DoublyNode[T]"] = None,
                 next: Optional["DoublyNode[T]"] = None) -> None:
        self.value = value
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        return f"DoublyNode({self.value!r})"


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[DoublyNode[T]] = None
        self.tail: Optional[DoublyNode[T]] = None
        self._size = 0

    def add_front(self, value: T) -> None:
        new_node = DoublyNode(value, None, self.head)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node

        self._size += 1

    def add_back(self, value: T) -> None:
        new_node = DoublyNode(value, self.tail, None)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def find(self, value: T) -> Optional[DoublyNode[T]]:
        current_node = self.head
        while current_node:
            if current_node.value == value:
                return current_node
            current_node = current_node.next
        return None

    def remove(self, value: T) -> None:
        current_node = self.head
        while current_node:
            if current_node.value == value:
                if current_node.prev:
                    current_node.prev.next = current_node.next
                else:
                    self.head = current_node.next

                if current_node.next:
                    current_node.next.prev = current_node.prev
                else:
                    self.tail = current_node.prev

                self._size -= 1

                current_node.next = None
                current_node.prev = None
                return None
            current_node = current_node.next

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current_node = self.head

        while current_node:
            yield current_node.value
            current_node = current_node.next

    def __contains__(self, value: T) -> bool:
        return self.find(value) is not None

    def __repr__(self) -> str:
        return "{}([{}])".format(
            self.__class__.__name__,
            ", ".join(repr(v) for v in self)
        )
