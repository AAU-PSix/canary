from os import linesep
from typing import List
from tree_sitter import Tree as _Tree
from .node import Node
from .tree_cursor import TreeCursor
from .file_point import FilePoint


class Tree:
    def __init__(self, tree: _Tree) -> None:
        self._tree = tree

    @property
    def root_node(self) -> Node:
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

    def replace(self, parser: "Parser", node: Node, new: str, encoding: str = "utf8") -> "Tree":
        source: str = self.text
        new_source: str = str(source[0: node.start_byte: 1] +
                              new +
                              source[node.end_byte:: 1])
        return parser.parse(new_source, self, encoding)

    def contents_of(self, node: Node) -> str:
        return str(self.text[node.start_byte: node.end_byte: 1])

    def insert_line(self, parser: "Parser", index: int, line: str, encoding: str = "utf8") -> "Tree":
        lines: List[str] = self.lines.copy()
        lines.insert(index, line)
        source: str = linesep.join(lines)
        return parser.parse(source)

    def append_line(self, parser: "Parser", index: int, line: str, encoding: str = "utf8") -> "Tree":
        return self.insert_line(parser, index + 1, line, encoding)

    def walk(self) -> TreeCursor:
        return TreeCursor(self._tree.walk())
