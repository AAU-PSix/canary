from ast import Tuple
from collections import namedtuple
from typing import List, Optional
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

class TreeCursor:
    def __init__(self, cursor: _TreeCursor) -> None:
        self._cursor = cursor

    @property
    def node(self) -> Node:
        return Node(self._cursor.node)

    def current_field_name(self) -> Optional[str]:
        return self._cursor.current_field_name()

    def goto_parent(self) -> bool:
        return self._cursor.goto_parent()

    def goto_first_child(self) -> bool:
        return self._cursor.goto_first_child()

    def goto_next_sibling(self) -> bool:
        return self._cursor.goto_next_sibling()

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

    def walk(self) -> TreeCursor:
        return TreeCursor(self._tree.walk())

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

#    def captures(self, node: Node) -> List[Tuple[Node, str]]:
#        return self._query.captures(node)

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