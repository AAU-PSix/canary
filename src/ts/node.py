from typing import List, Iterable

from tree_sitter import Node as _Node

from .file_point import FilePoint


class Node:
    def __init__(self, node: _Node) -> None:
        self._node = node

    @property
    def type(self) -> str:
        return self._node.type

    @property
    def is_named(self) -> bool:
        return self._node.is_named

    @property
    def is_missing(self) -> bool:
        return self._node.is_missing

    @property
    def has_changes(self) -> bool:
        return self._node.has_changes

    @property
    def has_error(self) -> bool:
        return self._node.has_error

    @property
    def start_point(self) -> FilePoint:
        point = self._node.start_point
        return FilePoint(point[0], point[1])

    @property
    def start_byte(self) -> int:
        return self._node.start_byte

    @property
    def end_point(self) -> FilePoint:
        point = self._node.end_point
        return FilePoint(point[0], point[1])

    @property
    def end_byte(self) -> int:
        return self._node.end_byte

    @property
    def sexp(self) -> str:
        return self._node.sexp()

    @property
    def children(self) -> List["Node"]:
        children: List[Node] = list()
        for child in self._node.children:
            children.append(Node(child))
        return children

    @property
    def named_children(self) -> List["Node"]:
        children: List[Node] = list()
        for native_child in self._node.children:
            child: Node = Node(native_child)
            if child.is_named: children.append(child)
        return children

    @property
    def child_count(self) -> int:
        return self._node.child_count

    @property
    def named_child_count(self) -> int:
        return self._node.named_child_count

    @property
    def next_sibling(self) -> "Node":
        result = self._node.next_sibling
        if result is None: return None
        return Node(result)

    @property
    def first_child(self) -> "Node":
        if self.child_count is 0: return None
        return self.children[0]

    @property
    def prev_sibling(self) -> "Node":
        result = self._node.prev_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def next_named_sibling(self) -> "Node":
        result = self._node.next_named_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def prev_named_sibling(self) -> "Node":
        result = self._node.prev_named_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def parent(self) -> "Node":
        result = self._node.parent
        if result is None:
            return None
        return Node(result)

    def child_by_field_id(self, id: int) -> "Node":
        result = self._node.child_by_field_id(id)
        if result is None:
            return None
        return Node(result)

    def child_by_field_name(self, name: str) -> "Node":
        result = self._node.child_by_field_name(name)
        if result is None:
            return None
        return Node(result)

    def is_descendent_of_type(self, type: str) -> bool:
        current: Node = self
        while current.parent is not None:
            if current.parent.type == type: return True
            current = current.parent
        return False

    def is_descendent_of_types(self, types: List[str]) -> str:
        current: Node = self
        while current.parent is not None:
            if current.parent.type in types: return current.parent.type
            current = current.parent
        return None

    def __eq__(self, other: "Node") -> bool:
        if other is None: return False
        return self.start_byte == other.start_byte and \
            self.end_byte == other.end_byte and \
            self.type == other.type

    def __ne__(self, other: "Node") -> bool:
        return not (self == other)

    def pre_order_traverse(self, named_only: bool = False) -> Iterable["Node"]:
        reached_root: bool = False
        curr: Node = self
        while not reached_root:
            if named_only and curr.is_named: yield curr
            elif not named_only: yield curr
            
            child: Node = curr.first_child
            if child is not None:
                curr = child
                continue
            
            sibling: Node = curr.next_sibling
            if sibling is not None:
                curr = sibling
                continue

            retracng: bool = True
            while retracng:
                if curr.parent is None:
                    retracng = False
                    reached_root = True
                if curr.next_sibling is not None:
                    retracng = False