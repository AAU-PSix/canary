from os import linesep
from typing import List

from tree_sitter import Parser as _Parser

from .node import Node
from .tree import Tree
from .language_library import LanguageLibrary
from .language_library import Language

class Parser:
    def __init__(self, parser: _Parser, language: Language = None):
        self._parser: _Parser = parser
        if language is not None:
            self.set_language(language)
        else:
            self._language = None

    @property
    def language(self) -> Language:
        return self._language

    @classmethod
    def create_with_language(cls, language: "Language") -> "Parser":
        parser: Parser = Parser(_Parser())
        parser.set_language(language)
        return parser

    def replace(self, tree: Tree, node: Node, new: str, encoding: str = "utf8") -> Tree:
        source: str = tree.text
        new_source: str = str(source[0: node.start_byte: 1] +
                              new +
                              source[node.end_byte:: 1])
        return self.parse(new_source, tree, encoding)

    def wrap(self, tree: Tree, node: Node, prefix: str = "", postfix: str = "", encoding: str = "utf8") -> Tree:
        replacement: str = prefix + tree.contents_of(node) + postfix
        return self.replace(tree, node, replacement, encoding)

    def insert(self, tree: Tree, node: Node, text: str, encoding: str = "utf8") -> Tree:
        replacement: str = text + tree.contents_of(node)
        return self.replace(tree, node, replacement, encoding)


    def append(self, tree: Tree, node: Node, text: str, encoding: str = "utf8") -> Tree:
        replacement: str = tree.contents_of(node) + text
        return self.replace(tree, node, replacement, encoding)

    def insert_line(self, tree: Tree, line_num: int, line: str, encoding: str = "utf8") -> Tree:
        lines: List[str] = tree.lines.copy()
        lines.insert(line_num, line)
        source: str = linesep.join(lines)
        return self.parse(source, tree, encoding)

    def append_line(self, tree: Tree, line_num: int, line: str, encoding: str = "utf8") -> Tree:
        return self.insert_line(tree, line_num + 1, line, encoding)

    def set_language(self, language: "Language") -> None:
        self._parser.set_language(language._language)
        self._language = language

    def parse_lines(self, lines: List[str], old_tree: Tree = None, encoding: str = "utf8") -> Tree:
        return self.parse(linesep.join(lines), old_tree, encoding)

    def parse(self, source: str, old_tree: Tree = None, encoding: str = "utf8") -> Tree:
        if old_tree is None:
            return Tree(self._parser.parse(bytes(source, encoding)))
        return Tree(self._parser.parse(bytes(source, encoding), old_tree._tree))

    @staticmethod
    def c() -> "Parser":
        return Parser.create_with_language(
            LanguageLibrary.c()
        )