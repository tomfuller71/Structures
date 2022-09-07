from typing import NamedTuple
from enum import Enum


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    NONE = 'None'
    BOTH = 'both'

    def opposite(self):
        return Direction.LEFT if self is Direction.RIGHT else Direction.RIGHT


class Node:
    def __init__(self, value) -> None:
        self.left: Node = None
        self.right: Node = None
        self.value: int = value

    @property
    def children_direction(self) -> Direction:
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
    replacement_value: int
    node_parent: Node
    count: int
    direction: Direction


class SearchResult(NamedTuple):
    did_find_value: bool
    parent_node: Node
    value_node: Node
    direction: Direction


class BST:
    def __init__(self, values=None) -> None:
        self.head: Node = None
        self.size = 0

        if isinstance(values, list):
            values.sort()
            values_length = len(values)
            if values_length == 1:
                self.head = Node(values.pop())
                self.size = 1
            elif values_length > 1:
                self.head = Node(values.pop(values_length // 2))
                self.size = BST.insert_list(self.head, values, 1)

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

        search: SearchResult = BST._parent_and_node_of_value(self.head, value)
        if not search.did_find_value:
            return False

        search_direction = search.value_node.children_direction
        if search_direction is Direction.NONE:
            setattr(search.parent_node, search.direction.value, None)
        else:
            successor: Successor = None
            if search_direction is not Direction.BOTH:
                successor = BST._successor(search.value_node, search_direction)
            else:
                left = BST._successor(search.value_node, Direction.LEFT)
                right = BST._successor(search.value_node, Direction.RIGHT)
                successor = left if left.count >= right.count else right

            search.value_node.value = successor.replacement_value
            setattr(successor.node_parent,
                    successor.direction.value, None)
        self.size -= 1
        return True

    def __len__(self):
        return self.size

    def __contains__(self, value):
        return BST.search(self.head, value) is not None

    def __repr__(self):
        return f"<{BST.__name__}>: [{BST.print_nodes(self.head)[:-2]}]"

    # Static methods of class used for traversal
    @staticmethod
    def print_nodes(node: Node, values=''):
        new_values = ''
        if node is None:
            return values
        new_values += BST.print_nodes(node.left)
        new_values += str(node.value) + ", "
        new_values += BST.print_nodes(node.right)
        return values + new_values

    @staticmethod
    def insert_list(head, lst, count=0):
        if len(lst) < 3:
            for value in lst:
                _, did_insert = BST.insert_node(head, value)
                if did_insert:
                    count += 1
        else:
            mid_index = len(lst) // 2
            new_head, did_insert = BST.insert_node(head, lst[mid_index])
            if did_insert:
                count += 1
            count += BST.insert_list(new_head, lst[0: mid_index])
            count += BST.insert_list(new_head, lst[mid_index + 1:])
        return count

    @staticmethod
    def _parent_and_node_of_value(node: Node, value) -> SearchResult:
        if node is None:
            return SearchResult(False, None, None, None)
        elif node.value == value:
            return SearchResult(True, node, node, node.children_direction)
        else:
            is_left = node.left is not None and node.left.value == value
            is_right = node.right is not None and node.right.value == value
            if is_left or is_right:
                direction = Direction.LEFT if is_left else Direction.RIGHT
                value_node = getattr(node, direction.value)
                return SearchResult(True, node, value_node, direction)
            elif node.value > value:
                return BST._parent_and_node_of_value(node.left, value)
            else:
                return BST._parent_and_node_of_value(node.right, value)

    @staticmethod
    def _successor(node: Node, direction: Direction):
        # initial step in direction
        prior_node = node
        successor_node = prior_node.get_child(direction)

        # now reverse as want min/max value for branch
        direction = direction.opposite()
        count = 0
        found_value = None

        while successor_node is not None:
            next_node = successor_node.get_child(direction)
            if next_node is None:
                found_value = successor_node.value
                break
            else:
                count += 1
                prior_node = successor_node
                successor_node = next_node

        # reverse back if never went down a level
        if count == 0:
            direction = direction.opposite()

        return Successor(found_value, prior_node, count, direction)

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

    @staticmethod
    def insert_node(head: Node, value):
        did_insert = True
        if head is None:
            head = Node(value)
        elif head.value > value:
            head.left, _ = BST.insert_node(head.left, value)
        elif head.value < value:
            head.right, _ = BST.insert_node(head.right, value)
        else:
            did_insert = False
        return (head, did_insert)


def main():
    values = [5, 8, 10, 54, 90, 4, 8, 1, 3, 12, 9, 17, 45, 80, 34, 27, 4]
    print(f"{values = }")
    tree = BST(values)
    print(f"{tree = }")
    print(f"{2 in tree = }")
    print(f"{20 in tree = }")
    print(f"{len(tree) = }")
    print(f"{tree.insert(99) = }")
    print(f"{tree = }")
    print(f"{len(tree) = }")
    print(f"{tree.delete(45) = }")
    print(f"{len(tree) = }")


if __name__ == "__main__":
    main()
