from collections import namedtuple
from typing import List
from tree_sitter.binding import (
    Parser as _Parser,
    Tree as _Tree,
    Node  as _Node,
    TreeCursor as _TreeCursor,
)

from .language import Language

FilePoint = namedtuple('Point', ['line', 'char'])

class Range:
    def __init__(self) -> None:
        pass

class Cursor:
    def __init__(self) -> None:
        pass

class Node:
    def __init__(self, node: _Node) -> None:
        self._node = node

    @property
    def type(self) -> str:
        return self._node.type

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

class Tree:
    def __init__(self, tree: _Tree) -> None:
        self._tree = tree

    @property
    def root_node(self) -> Node:
        return Node(self._tree.root_node)

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

    def walk(self) -> Cursor:
        return _TreeCursor(self._tree.walk())

    def get_changed_ranges(self, new_tree: "Tree") -> any:
        return self._tree.get_changed_ranges(new_tree._tree)
        ranges: List[Range] = list()
        for changed_range in self._tree.get_changed_ranges(new_tree._tree):
            pass

class Parser:
    def __init__(self, parser: _Parser, language: Language = None):
        self._parser: _Parser = parser
        if language is not None:
            self.set_language(language)

    @classmethod
    def create_with_language(cls, language: Language) -> "Parser":
        parser: Parser = Parser(_Parser())
        parser.set_language(language)
        return parser

    def __init__(self, parser: _Parser) -> None:
        self._parser = parser

    def set_language(self, language: Language) -> None:
        self._parser.set_language(language._language)

    def parse(self, source: str, old_tree: Tree = None, encoding: str = "utf8") -> Tree:
        if old_tree is None:
            return Tree(self._parser.parse(bytes(source, encoding)))
        return Tree(self._parser.parse(bytes(source, encoding), old_tree._tree))