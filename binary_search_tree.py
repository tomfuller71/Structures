from math import inf
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
        self.__head: Node = None
        self.__size = 0
        self.__min = inf
        self.__max = -inf

        if values and isinstance(values, list):
            values.sort()
            for value in BST._order_lst_to_insert(values):
                self.insert(value)

    def insert(self, value) -> bool:
        if value < self.__min:
            self.__min = value
        elif value > self.__max:
            self.__max = value

        node, did_insert = BST._insert_node(self.__head, value)
        if did_insert:
            self.__size += 1
        if self.__head is None:
            self.__head = node

        return did_insert

    def delete(self, value) -> bool:
        """Deletes node of matching value from larger tree branch (balancing)"""
        if self.__head is None:
            return False

        searched_node: Node = BST._find(self.__head, value)
        if searched_node is None:
            return False

        search_direction = searched_node.children
        if search_direction is Direction.NONE:
            if searched_node.parent is None:
                self.__head = None
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
        self.__size -= 1
        return True

    def pprint(self, from_value=None):
        head = self.__head if from_value is None else BST._find(from_value)
        depth = BST._tree_depth_from(head)
        if depth > 6:
            print(f"Tree {depth = }, to large to print")

        val_width = max(len(str(self.__max)), len(str(self.__min)))
        pad = val_width * " "
        row_width = ((2 ** (depth + 1)) - 1) * val_width

        level_values = [[None for _ in range(2 ** n)]
                        for n in range(depth + 1)]
        for node, level in self._yield_pprint_values(head):
            if level == 0:
                level_values[0][0] = node.value
                continue

            index = 0
            tracking_node = head
            step = len(level_values[level]) // 2
            for _ in range(level):
                if node.value > tracking_node.value:
                    index += step
                    tracking_node = tracking_node.right
                else:
                    tracking_node = tracking_node.left
                step //= 2

            level_values[level][index] = node.value

        for lvl, values in enumerate(level_values):
            spacing = ((2 ** (depth - lvl + 1)) - 1) * pad
            lvl_str = spacing.join(
                (pad if value is None else str(value).center(val_width)
                 for value in values)
            )
            lvl_str = f"Level {lvl + 1}: " + lvl_str.center(row_width)
            print(lvl_str)

    def _yield_pprint_values(self, from_node):
        level_nodes = [(from_node, 0)]

        while level_nodes:
            node, level = level_nodes.pop(0)
            if node.left:
                level_nodes.append((node.left, level + 1))
            if node.right:
                level_nodes.append((node.right, level + 1))
            yield node, level

    def __len__(self):
        return self.__size

    def __contains__(self, value):
        return BST._find(self.__head, value) is not None

    def __min__(self):
        return self.__min

    def __max__(self):
        return self.__max

    def __repr__(self):
        value_strs = (str(e) for e in self)
        return f"<{BST.__name__}>: [{', '.join(value_strs)}]"

    def __iter__(self):
        return BST._yield_values_in_order(self.__head)

    # Static methods of class
    @staticmethod
    def _yield_values_in_order(node: Node):
        if node is None:
            return

        if node.left:
            for value in BST._yield_values_in_order(node.left):
                yield value

        yield node.value

        if node.right:
            for value in BST._yield_values_in_order(node.right):
                yield value

    @staticmethod
    def _tree_depth_from(head):
        level_nodes = [(head, 0)]
        max_level = 0
        while level_nodes:
            node, level = level_nodes.pop(0)
            if level > max_level:
                max_level = level
            if node.left:
                level_nodes.append((node.left, level + 1))
            if node.right:
                level_nodes.append((node.right, level + 1))

        return max_level

    @staticmethod
    def _insert_node(head: Node, value, parent: Node = None):
        did_insert = True
        if head is None:
            head = Node(value)
            head.parent = parent
        elif head.value > value:
            head.left, did_insert = BST._insert_node(head.left, value, head)
        elif head.value < value:
            head.right, did_insert = BST._insert_node(head.right, value, head)
        else:
            did_insert = False
        return head, did_insert

    @staticmethod
    def _order_lst_to_insert(lst):
        mid_index = len(lst) // 2
        yield lst[mid_index]
        if left := lst[0: mid_index]:
            for value in BST._order_lst_to_insert(left):
                yield value
        if right := lst[mid_index + 1:]:
            for value in BST._order_lst_to_insert(right):
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
    def _find(node: Node, value) -> Node:
        if node is None:
            return None
        if node.value == value:
            return node
        elif node.value > value:
            return BST._find(node.left, value)
        else:
            return BST._find(node.right, value)


@time_function
def main():
    values = [5, 8, 10, 54, 90, 4, 1, 3, 12, 9, 17, 45, 80, 34, 27]
    print("\nDemonstration of BST class functionality:\n")
    print(f" - Can be instantiate from unordered {values = }\n")
    tree = BST(values)

    print(" - Provides insertion without duplication:")
    print(f"\tInsert new value succeeds: {tree.insert(52) = }")
    print(f"\tInsert new value succeeds: {tree.insert(53) = }")
    print(f"\tInsert duplicate value fails: {tree.insert(5) = }\n")
    print(" - Provides deletion:")
    print(f"\tDelete succeeds: {tree.delete(8) = }")
    print(f"\tDelete fails: {tree.delete(1000) = }\n")

    print("\n - Implements standard object special methods:")
    print(f"\tString repr (ordered): {tree = }\n")
    print(f"\tBool of tree contains:{2 not in tree = }")
    print(f"\t\tNegative case: {2 not in tree = }")
    print(f"\t\tPositive case: {80 in tree = }\n")
    print(f"\tLength: {len(tree) = }\n")
    print(f"\tMin value: {min(tree) = }")
    print(f"\tMax value:{max(tree) = }\n")

    print(" - Provides pprint of tree structure: \n")
    tree.pprint()
    print("\n")

    print(" - Deletion partially re-balances tree:")
    print(f"\t{tree.delete(45) = }\n")
    tree.pprint()
    print("\n")


if __name__ == "__main__":
    main()
