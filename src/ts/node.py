from typing import List, Optional

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
    def child_count(self) -> int:
        return self._node.child_count

    @property
    def named_child_count(self) -> int:
        return self._node.named_child_count

    @property
    def next_sibling(self) -> Optional["Node"]:
        result = self._node.next_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def prev_sibling(self) -> Optional["Node"]:
        result = self._node.prev_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def next_named_sibling(self) -> Optional["Node"]:
        result = self._node.next_named_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def prev_named_sibling(self) -> Optional["Node"]:
        result = self._node.prev_named_sibling
        if result is None:
            return None
        return Node(result)

    @property
    def parent(self) -> Optional["Node"]:
        result = self._node.parent
        if result is None:
            return None
        return Node(result)

    def child_by_field_id(self, id: int) -> Optional["Node"]:
        result = self._node.child_by_field_id(id)
        if result is None:
            return None
        return Node(result)

    def child_by_field_name(self, name: str) -> Optional["Node"]:
        result = self._node.child_by_field_name(name)
        if result is None:
            return None
        return Node(result)