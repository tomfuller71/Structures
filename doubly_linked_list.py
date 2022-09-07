class Node:
    def __init__(self, value) -> None:
        self.next: Node = None
        self.previous: Node = None
        self.value = value


class LinkedList:
    def __init__(self) -> None:
        init_node = Node(None)
        self.__head: Node = init_node
        self.__tail: Node = init_node
        self.__size = 0

    def append(self, value):
        if self.__size == 0:
            self.__head.value = value
        else:
            new_node = Node(value)
            new_node.previous = self.__tail
            self.__tail.next = new_node
            self.__tail = new_node
        self.__size += 1

    def pop(self):
        value = self.__tail.value
        if self.__size == 0:
            self.__tail.value = None
        else:
            self.__tail = self.__tail.previous
            self.__tail.next = None

        self.__size -= 1

        if self.__size == 0:
            self.__head = self.__tail

        return value

    def __get_ith_node__(self, i):
        if not (0 <= i < self.__size):
            raise IndexError
        current_node = self.__head
        for _ in range(i):
            current_node = current_node.next

        return current_node

    def __iter__(self):
        self.iter_node = self.__head
        return self

    def __next__(self):
        if self.iter_node is None:
            raise StopIteration
        else:
            value = self.iter_node.value
            self.iter_node = self.iter_node.next
            return value

    def __len__(self):
        return self.__size

    def __getitem__(self, i):
        return self.__get_ith_node__(i).value

    def __setitem__(self, i, value):
        self.__get_ith_node__(i).value = value

    def __repr__(self) -> str:
        values = list(self)
        return str(values)


def main():
    linked = LinkedList()
    print("When empty:")
    print(f"\t{bool(linked) = }")

    print(f"\t{len(linked) = }\n")
    for i in range(1, 101):
        linked.append(i)

    print("When filled with range(1:101):")
    print(f"\t{bool(linked) = }")
    print(f"\t{len(linked) = }\n")

    print(f" __getitem__: {linked[1] = }")
    print(f" __setitem__: linked[50] = 1000")
    linked[50] = 1000
    print(f"\t{linked[50] = }\n")

    print(f"Using .pop(): {linked.pop() = }\n")

    print("__repr__:", linked, "\n")

    print(f"Using __iter__ and __next__:")
    print(f"\t{sum(linked) = }")


if __name__ == "__main__":
    main()
