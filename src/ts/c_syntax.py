from typing import Iterable
from .syntax import Field, NodeType, Syntax
from .node import Node

class CField(Field):
    PATH = "path"
    NAME = "name"
    VALUE = "value"
    PARAMETERS = "parameters"
    directive = "directive"
    argument = "argument"
    OPERATOR = "operator"
    FUNCTION = "function"
    ARGUMENT = "argument"
    ARGUMENTS = "arguments"
    LEFT = "left"
    RIGHT = "right"
    DECLARATOR = "declarator"
    BODY = "body"
    PREFIX = "prefix"
    SIZE = "size"
    TYPE = "type"
    LABEL = "label"
    CONDITION = "condition"
    CONSEQUENCE = "consequence"
    ALTERNATIVE = "alternative"
    INITIALIZER = "initializer"
    INDEX = "index"
    DESIGNATOR = "designator"
    UPDATE = "update"

class CNodeType(NodeType):
    # Binary expression operators
    PLAIN_ASSIGNMENT = "="
    ARITHMETIC_ADDITION = "+"
    ARITHMETIC_SUBTRACTION = "-"
    ARITHMETIC_MULTIPLICATION = "*"
    ARITHMETIC_DIVISION = "/"
    ARITHMETIC_MODULO = "%"
    BITWISE_OR = "|"
    BITWISE_AND = "&"
    BITWISE_XOR = "^"
    SHIFT_LEFT = "<<"
    SHIFT_RIGHT = ">>"
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    RELATIONAL_LESS_THAN = "<"
    RELATIONAL_GREATER_THAN = ">"
    RELATIONAL_LESS_THAN_OR_EQUAL = "<="
    RELATIONAL_GREATER_THAN_OR_EQUAL = ">="
    RELATIONAL_EQUAL = "=="
    RELATIONAL_NOT_EQUAL = "!="
    ARITHMETIC_COMPOUND_ADDITION = "+="
    ARITHMETIC_COMPOUND_SUBTRACTION = "-="
    ARITHMETIC_COMPOUND_MULTIPLICATION = "*="
    ARITHMETIC_COMPOUND_DIVISION = "/="
    ARITHMETIC_COMPOUND_MODULO = "%="
    BITWISE_COMPOUND_OR = "|="
    BITWISE_COMPOUND_AND = "&="
    BITWISE_COMPOUND_XOR = "^="
    SHIFT_COMPOUND_LEFT = "<<="
    SHIFT_COMPOUND_RIGHT = ">>="
    # Literals
    IDENTIFIER = "identifier"
    # Constructs
    EXPRESSION_STATEMENT = "expression_statement"
    DECLARATION = "declaration"
    IF_STATEMENT = "if_statement"
    WHILE_STATEMENT = "while_statement"
    TRANSLATION_UNIT = "translation_unit"
    COMPOUND_STATEMENT = "compound_statement"
    DO_STATEMENT = "do_statement"
    FOR_STATEMENT = "for_statement"
    SWITCH_STATEMENT = "switch_statement"
    BREAK_STATEMENT = "break_statement"
    CONTINUE_STATEMENT = "continue_statement"
    RETURN_STATEMENT = "return_statement"
    LABELED_STATEMENT = "labeled_statement"
    GOTO_STATEMENT = "goto_statement"

class CSyntax(Syntax):
    @property
    def plain_assignment(self) -> Iterable[CNodeType]:
        return [
            CNodeType.PLAIN_ASSIGNMENT,
        ]

    @property
    def arithmetic_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.ARITHMETIC_ADDITION,
            CNodeType.ARITHMETIC_SUBTRACTION,
            CNodeType.ARITHMETIC_MULTIPLICATION,
            CNodeType.ARITHMETIC_DIVISION,
            CNodeType.ARITHMETIC_MODULO,
        ]

    @property
    def bitwise_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.BITWISE_OR,
            CNodeType.BITWISE_AND,
            CNodeType.BITWISE_XOR,
        ]

    @property
    def shift_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.SHIFT_LEFT,
            CNodeType.SHIFT_RIGHT,
        ]

    @property
    def logical_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.LOGICAL_AND,
            CNodeType.LOGICAL_OR,
        ]

    @property
    def relational_opearators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.RELATIONAL_GREATER_THAN,
            CNodeType.RELATIONAL_GREATER_THAN_OR_EQUAL,
            CNodeType.RELATIONAL_LESS_THAN,
            CNodeType.RELATIONAL_LESS_THAN_OR_EQUAL,
            CNodeType.RELATIONAL_EQUAL,
            CNodeType.RELATIONAL_NOT_EQUAL,
        ]

    @property
    def arithmetic_compound_assignment(self) -> Iterable[CNodeType]:
        return [
            CNodeType.ARITHMETIC_COMPOUND_ADDITION,
            CNodeType.ARITHMETIC_COMPOUND_SUBTRACTION,
            CNodeType.ARITHMETIC_COMPOUND_MULTIPLICATION,
            CNodeType.ARITHMETIC_COMPOUND_DIVISION,
            CNodeType.ARITHMETIC_COMPOUND_MODULO,
        ]

    @property
    def bitwise_compound_assignment(self) -> Iterable[CNodeType]:
        return [
            CNodeType.BITWISE_COMPOUND_OR,
            CNodeType.BITWISE_COMPOUND_AND,
            CNodeType.BITWISE_COMPOUND_XOR,
        ]

    @property
    def shift_compound_assignment(self) -> Iterable[CNodeType]:
        return [
            CNodeType.SHIFT_COMPOUND_LEFT,
            CNodeType.SHIFT_COMPOUND_RIGHT,
        ]

    @property
    def assignment_query(self) -> str:
        return "((assignment_expression) @exp)"

    @property
    def compound_assignment_query(self) -> str:
        return "((assignment_expression) @exp)"

    @property
    def binary_expression_query(self) -> str:
        return '((binary_expression) @exp)' + self.assignment_query

    @property
    def function_declaration_query(self) -> str:
        return "((function_definition) @def)"

    @property
    def struct_declaration_query(self) -> str:
        return '((struct_specifier) @spec)'

    @property
    def if_statement_query(self) -> str:
        return '(if_statement) @if'

    def get_binary_expression_operator(self, node: Node) -> Node:
        return node.children[1]

    def get_function_declaration(self, node: Node) -> Node:
        return node

    def get_struct_declaration(self, node: Node) -> Node:
        return node

    def get_if_declaration(self, node: Node) -> Node:
        return node

    def node_field(self, node_type: str) -> CNodeType:
        return CNodeType(node_type)