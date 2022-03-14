from os import linesep
from collections import namedtuple
from typing import Callable, Iterable, List, Optional, Tuple
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

    def reset(self):
        while self.goto_parent(): pass

    def pre_order_traverse(self) -> Iterable[Node]:
        reached_root: bool = False
        while not reached_root:
            yield self.node
            if self.goto_first_child(): continue
            if self.goto_next_sibling(): continue

            retracng: bool = True
            while retracng:
                if not self.goto_parent():
                    retracng = False
                    reached_root = True
                if self.goto_next_sibling():
                    retracng = False


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


class Capture:
    def __init__(self, capture: List[Tuple[Node, str]]) -> None:
        self._capture = capture

    def __iter__(self) -> any:
        return self._capture.__iter__()

    def __next__(self) -> Tuple[Node, str]:
        return self._capture.__next__()

    def __getitem__(self, idx: int) -> Tuple[Node, str]:
        return self._capture[idx]

    def __len__(self) -> int:
        return len(self._capture)

    def first(self) -> Tuple[Node, str]:
        return self._capture[0]

    def last(self) -> Tuple[Node, str]:
        return self._capture[-1]

    def nodes(self, func: Callable[[Node], Node] = lambda node: node) -> List[Node]:
        nodes: List[Node] = list()
        for result in self:
            nodes.append(func(result[0]))
        return nodes

    @staticmethod
    def create_from_native_capture(capture: Tuple[any, str]) -> "Capture":
        result: List[Tuple[Node, str]] = list()
        for capture in capture:
            capture_node: Node = Node(capture[0])
            capture_field: str = capture[1]
            capture_tuple: Tuple[Node, str] = (capture_node, capture_field)
            result.append(capture_tuple)
        return Capture(result)


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

class Query:
    def __init__(self, query: _Query) -> None:
        self._query = query

    def matches(self, node: Node):
        """Get a list of all the matches within the given node

        Args:
            node (Node): The root node to query from
        """
        self._query.macthes(node._node)

    def captures(
        self,
        node: Node,
        start_point: FilePoint = None,
        end_point: FilePoint = None,
    ) -> Capture:
        if start_point is None or end_point is None:
            native_capture = self._query.captures(node._node)
        else:
            native_capture = self._query.captures(node._node, start_point, end_point)
        return Capture.create_from_native_capture(native_capture)


class Syntax:
    def __init__(
        self,
        # Binary expression operators
        plain_assignment: List[str] = None,
        arithmetic_operators: List[str] = None,
        bitwise_operators: List[str] = None,
        shift_operators: List[str] = None,
        logical_operators: List[str] = None,
        relational_opearators: List[str] = None,
        arithmetic_compound_assignment: List[str] = None,
        bitwise_compound_assignment: List[str] = None,
        shift_compound_assignment: List[str] = None,
        # Predefined queries
        assignment_query: str = None,
        compound_assignment_query: str = None,
        binary_expression_query: str = None,
        function_declaration_query: str = None,
        struct_declaration_query: str = None,
        # Query result processors
        get_binary_expression_operator: Callable[[Node], Node] = None,
        get_function_declaration: Callable[[Node], Node] = None,
        get_struct_declaration: Callable[[Node], Node] = None,
    ) -> None:
        # Binary expression operators
        self._plain_assignment = plain_assignment
        self._arithmetic_operators = arithmetic_operators
        self._bitwise_operators = bitwise_operators
        self._shift_operators = shift_operators
        self._logical_operators = logical_operators
        self._relational_opearators = relational_opearators
        self._arithmetic_compound_assignment = arithmetic_compound_assignment
        self._bitwise_compound_assignment = bitwise_compound_assignment
        self._shift_compound_assignment = shift_compound_assignment
        # Predefined queries
        self._assignment_query = assignment_query
        self._compound_assignment_query = compound_assignment_query
        self._binary_expression_query = binary_expression_query
        self._function_declaration_query = function_declaration_query
        self._struct_declaration_query = struct_declaration_query
        # Query result processors
        self._get_binary_expression_operator = get_binary_expression_operator
        self._get_function_declaration = get_function_declaration
        self._get_struct_declaration = get_struct_declaration

    @property
    def plain_assignment(self) -> str:
        return self._plain_assignment

    @property
    def arithmetic_operators(self) -> List[str]:
        return self._arithmetic_operators

    @property
    def bitwise_operators(self) -> List[str]:
        return self._bitwise_operators

    @property
    def shift_operators(self) -> List[str]:
        return self._shift_operators

    @property
    def logical_operators(self) -> List[str]:
        return self._logical_operators

    @property
    def relational_opearators(self) -> List[str]:
        return self._relational_opearators

    @property
    def arithmetic_compound_assignment(self) -> List[str]:
        return self._arithmetic_compound_assignment

    @property
    def bitwise_compound_assignment(self) -> List[str]:
        return self._bitwise_compound_assignment

    @property
    def shift_compound_assignment(self) -> List[str]:
        return self._shift_compound_assignment

    @property
    def query_assignment(self) -> str:
        return self._assignment_query

    @property
    def query_compound_assignment(self) -> str:
        return self._compound_assignment_query

    @property
    def query_binary_expression(self) -> str:
        return self._binary_expression_query

    @property
    def query_function_declaration(self) -> str:
        return self._function_declaration_query

    @property
    def query_struct_declaration(self) -> str:
        return self._struct_declaration_query

    def get_binary_expression_operator(self, node: Node) -> Node:
        return self._get_binary_expression_operator(node)

    def get_function_declaration(self, node: Node) -> Node:
        return self._get_function_declaration(node)

    def get_struct_declaration(self, node: Node) -> Node:
        return self._get_struct_declaration(node)

    @staticmethod
    def c() -> "Syntax":
        # Binary expression operators
        plain_assignment: List[str] = ['=']
        arithmetic_operators: List[str] = ['+', '-', '*', '/', '%']
        bitwise_operators: List[str] = ['|', '&', '^']
        shift_operators: List[str] = ['<<', '>>']
        logical_operators: List[str] = ['&&', '||']
        relational_opearators: List[str] = ['>', '>=', '<', '<=', '==', '!=']
        arithmetic_compound_assignment: List[str] = [operator + plain_assignment[0]
                                                     for operator in arithmetic_operators]
        bitwise_compound_assignment: List[str] = [operator + plain_assignment[0]
                                                  for operator in bitwise_operators]
        shift_compound_assignment: List[str] = [operator + plain_assignment[0]
                                                for operator in shift_operators]

        # Predefined queries
        assignment_query = '((assignment_expression) @exp)'
        compound_assignment_query = '((assignment_expression) @exp)'
        binary_expression_query = '((binary_expression) @exp)'
        function_declaration_query = "((function_definition) @def)"
        struct_declaration_query = '((struct_specifier) @spec)'

        # Query result processors (Infix)
        get_binary_expression_operator: Callable[[Node], Node] = lambda node: node.children[1]
        get_function_declaration: Callable[[Node], Node] = lambda node: node
        get_struct_declaration: Callable[[Node], Node] = lambda node: node

        return Syntax(
            plain_assignment = plain_assignment,
            arithmetic_operators = arithmetic_operators,
            bitwise_operators = bitwise_operators,
            shift_operators = shift_operators,
            logical_operators = logical_operators,
            relational_opearators = relational_opearators,
            arithmetic_compound_assignment = arithmetic_compound_assignment,
            bitwise_compound_assignment = bitwise_compound_assignment,
            shift_compound_assignment = shift_compound_assignment,

            assignment_query = assignment_query,
            compound_assignment_query = compound_assignment_query,
            binary_expression_query = binary_expression_query,
            function_declaration_query = function_declaration_query,
            struct_declaration_query = struct_declaration_query,

            get_binary_expression_operator = get_binary_expression_operator,
            get_function_declaration = get_function_declaration,
            get_struct_declaration = get_struct_declaration,
        )


class Language:
    def __init__(self, syntax: Syntax, language: _Language) -> None:
        self._language = language
        self._syntax = syntax

    @property
    def syntax(self) -> Syntax:
        return self._syntax

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
    def build() -> None:
        _Language.build_library(
            LanguageLibrary.full_build_path(),
            [
                f'{LanguageLibrary.vendor_path()}/tree-sitter-c',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-cpp',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-go',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-javascript',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-python',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-rust',
            ]
        )

    @staticmethod
    def c() -> Language:
        return Language(
            Syntax.c(),
            _Language(LanguageLibrary.full_build_path(), 'c')
        )

    @staticmethod
    def cpp() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'cpp')
        )

    @staticmethod
    def go() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'go')
        )

    @staticmethod
    def js() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'javascript')
        )

    @staticmethod
    def python() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'python')
        )

    @staticmethod
    def rust() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'rust')
        )
