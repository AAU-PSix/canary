from os import linesep
from typing import List

from tree_sitter import Parser as _Parser

from .tree import Tree
from .language_library import LanguageLibrary


class Parser:
    def __init__(self, parser: _Parser, language: "Language" = None):
        self._parser: _Parser = parser
        if language is not None:
            self.set_language(language)

    @property
    def language(self) -> "Language":
        return self._language

    @classmethod
    def create_with_language(cls, language: "Language") -> "Parser":
        parser: Parser = Parser(_Parser())
        parser.set_language(language)
        return parser

    def __init__(self, parser: _Parser) -> None:
        self._parser = parser

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