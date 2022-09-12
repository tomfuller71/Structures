from typing import NamedTuple
from enum import Enum
from utils import time_function


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    NONE = 'None'
    BOTH = 'both'

    def opposite(self):
        return Direction.LEFT if self is Direction.RIGHT else Direction.RIGHT


class Node:
    def __init__(self, value=None) -> None:
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None
        self.value: int = value

    @property
    def children(self) -> Direction:
        if self.left is not None and self.right is not None:
            return Direction.BOTH
        elif self.right is not None:
            return Direction.RIGHT
        elif self.left is not None:
            return Direction.LEFT
        else:
            return Direction.NONE

    def get_child(self, direction: Direction):
        if direction is Direction.NONE:
            return None
        elif direction is Direction.BOTH:
            return self.left, self.right
        else:
            return getattr(self, direction.value)

    def __repr__(self):
        return str(self.value)


class Successor(NamedTuple):
    node: Node
    direction: Direction
    count: int


class BST:
    def __init__(self, values=None) -> None:
        self.head: Node = None
        self.size = 0

        if values and isinstance(values, list):
            values.sort()
            for value in BST.insert_order(values):
                self.insert(value)

    def insert(self, value) -> bool:
        node, did_insert = BST.insert_node(self.head, value)
        if did_insert:
            self.size += 1
        if self.head is None:
            self.head = node
        return did_insert

    def delete(self, value) -> bool:
        """Deletes node of matching value from larger tree branch (balancing)"""
        if self.head is None:
            return False

        searched_node: Node = BST.search(self.head, value)
        search_direction = searched_node.children
        if not searched_node:
            return False
        elif search_direction is Direction.NONE:
            if searched_node.parent is None:
                self.head = None
            else:
                if searched_node.parent.left is searched_node:
                    searched_node.parent.left = None
                else:
                    searched_node.parent.right = None
        else:
            successor: Successor = None
            if search_direction is not Direction.BOTH:
                successor = BST._successor(searched_node, search_direction)
            else:
                left = BST._successor(searched_node, Direction.LEFT)
                right = BST._successor(searched_node, Direction.RIGHT)
                successor = left if left.count >= right.count else right

            searched_node.value = successor.node.value
            setattr(successor.node.parent, successor.direction.value, None)
        self.size -= 1
        return True

    def __len__(self):
        return self.size

    def __contains__(self, value):
        return BST.search(self.head, value) is not None

    def __repr__(self):
        value_strs = (str(e) for e in self)
        return f"<{BST.__name__}>: [{', '.join(value_strs)}]"

    def __iter__(self):
        return BST.yield_values(self.head)

    # Static methods of class
    @staticmethod
    def yield_values(node: Node):
        if node is None:
            return

        if node.left:
            for value in BST.yield_values(node.left):
                yield value

        yield node.value

        if node.right:
            for value in BST.yield_values(node.right):
                yield value

    @staticmethod
    def insert_node(head: Node, value, parent: Node = None):
        did_insert = True
        if head is None:
            head = Node(value)
            head.parent = parent
        elif head.value > value:
            head.left, did_insert = BST.insert_node(head.left, value, head)
        elif head.value < value:
            head.right, did_insert = BST.insert_node(head.right, value, head)
        else:
            did_insert = False
        return head, did_insert

    @staticmethod
    def insert_order(lst):
        mid_index = len(lst) // 2
        yield lst[mid_index]
        if left := lst[0: mid_index]:
            for value in BST.insert_order(left):
                yield value
        if right := lst[mid_index + 1:]:
            for value in BST.insert_order(right):
                yield value

    @staticmethod
    def _successor(node: Node, direction: Direction):
        prior = node
        node = node.get_child(direction)
        # now reverse as want min/max value for branch
        direction = direction.opposite()
        count = 0

        while node is not None:
            count += 1
            prior = node
            node = node.get_child(direction)

        # reverse back if never went down a level
        if count == 0:
            direction = direction.opposite()

        return Successor(prior, direction, count)

    @staticmethod
    def search(node: Node, value) -> Node:
        if node is None:
            return None
        if node.value == value:
            return node
        elif node.value > value:
            return BST.search(node.left, value)
        else:
            return BST.search(node.right, value)


@time_function
def main():
    values = [5, 8, 10, 54, 90, 4, 8, 1, 3, 12, 9, 17, 45, 80, 34, 27]

    print(f"{values = }")
    print(f"{len(values) = }")
    tree = BST(values)
    print(f"{tree = }")
    print(f"{2 not in tree = }")
    print(f"{80 in tree = }")
    print(f"{len(tree) = }")
    print(f"{tree.insert(99) = }")
    print(f"{tree = }")
    print(f"{len(tree) = }")
    print(f"{tree.delete(45) = }")
    print(f"{len(tree) = }")
    print(f"{tree = }")


if __name__ == "__main__":
    main()
