from typing import Iterable, List
from tree_sitter import Tree as _Tree

from .node import Node
from .tree_cursor import TreeCursor
from .file_point import FilePoint


class Tree:
    def __init__(self, tree: _Tree) -> None:
        self._tree = tree

    @property
    def root(self) -> Node:
        return Node(self._tree.root_node)

    @property
    def text(self) -> str:
        return self._tree.text.decode("utf-8")

    @property
    def lines(self) -> List[str]:
        return self.text.splitlines()

    def edit(
            self,
            start_byte: int,
            old_end_byte: int,
            new_end_byte: int,
            start_point: FilePoint,
            old_end_point: FilePoint,
            new_end_point: FilePoint,
    ) -> None:
        self._tree.edit(
            start_byte,
            old_end_byte,
            new_end_byte,
            start_point,
            old_end_point,
            new_end_point,
        )

    def contents_of(self, node: Node) -> str:
        return str(self.text[node.start_byte: node.end_byte: 1])

    def walk(self) -> TreeCursor:
        return TreeCursor(self._tree.walk())

    def line_traverse(self) -> Iterable[str]:
        lines: List[str] = self.lines
        for line in lines:
            yield line
