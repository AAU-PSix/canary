from collections import namedtuple
from typing import List
from tree_sitter import Language as _Language
from tree_sitter.binding import (
    Parser as _Parser,
    Tree as _Tree,
    Node  as _Node,
    TreeCursor as _TreeCursor,
    Query as _Query,
)

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
    def __init__(self, parser: _Parser, language: "Language" = None):
        self._parser: _Parser = parser
        if language is not None:
            self.set_language(language)

    @classmethod
    def create_with_language(cls, language: "Language") -> "Parser":
        parser: Parser = Parser(_Parser())
        parser.set_language(language)
        return parser

    def __init__(self, parser: _Parser) -> None:
        self._parser = parser

    def set_language(self, language: "Language") -> None:
        self._parser.set_language(language._language)

    def parse(self, source: str, old_tree: Tree = None, encoding: str = "utf8") -> Tree:
        if old_tree is None:
            return Tree(self._parser.parse(bytes(source, encoding)))
        return Tree(self._parser.parse(bytes(source, encoding), old_tree._tree))

class Query:
    def __init__(self, query: _Query) -> None:
        self._query = query

    def matches(self, node: Node):
        """Get a list of all the matches within the given node

        Args:
            node (Node): The root node to query from
        """
        self._query(node._node)

    def captures(self, node: Node):
        # TODO: Not tested, since the parser isnt wrapped yet.
        return self._query.captures(node)

class Language:
    def __init__(self, language: _Language) -> None:
        self._language = language

    @property
    def id(self) -> int:
        return self._language.language_id
    
    @property
    def name(self):
        return self._language.name

    def field_id_for_name(self, name: str) -> int:
        """Returns the id of a field found in 'grammer.js' as a 'field' function call

        Args:
            name (str): The name of the field, also the first parameter in the function call

        Returns:
            int: The int id of the field
        """
        return self._language.field_id_for_name(name)

    def query(self, source: str) -> Query:
        """Creates a query from the soruce for a given language

        Args:
            source (str): The query source

        Returns:
            Query: A query for the given language
        """
        return Query(self._language.query(source))

class LanguageLibrary:
    @staticmethod
    def vendor_path() -> str:
        return './vendor'

    @staticmethod
    def build_path() -> str:
        return './build'

    @staticmethod
    def build_file() -> str:
        return 'my-languages.so'

    @staticmethod
    def full_build_path() -> str:
        return f'{LanguageLibrary.build_path()}/{LanguageLibrary.build_file()}'

    @staticmethod
    def build() -> str:
        _Language.build_library(
            LanguageLibrary.full_build_path(),
            [ f'{LanguageLibrary.vendor_path()}/tree-sitter-javascript' ]
        )

    @staticmethod
    def js() -> Language:
        return Language(
            _Language(LanguageLibrary.full_build_path(), 'javascript')
        )