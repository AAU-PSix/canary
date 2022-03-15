from typing import List, Callable

from .node import Node


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
        get_get_function_declaration: Callable[[Node], Node] = None,
        get_get_struct_declaration: Callable[[Node], Node] = None,
        get_get_if_declaration: Callable[[Node], Node] = None,
        if_declaration_query: str = None
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
        self._get_function_declaration = get_get_function_declaration
        self._get_struct_declaration = get_get_struct_declaration
        self._get_get_if_declaration = get_get_if_declaration
        self._get_if_query = if_declaration_query

    @property
    def plain_assignment(self) -> List[str]:
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
    def query_if_statement(self) -> str:
        return self._get_if_query


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
        binary_expression_query = '((binary_expression) @exp)' + assignment_query
        function_declaration_query = "((function_definition) @def)"
        struct_declaration_query = '((struct_specifier) @spec)'
        if_declaration_query = '(if_statement) @if'

        # Query result processors (Infix)
        get_binary_expression_operator: Callable[[Node], Node] = lambda node: node.children[1]
        get_function_declaration: Callable[[Node], Node] = lambda node: node
        get_struct_declaration: Callable[[Node], Node] = lambda node: node
        get_if_declaration: Callable[[Node], Node] = lambda node: node

        return Syntax(
            plain_assignment,
            arithmetic_operators,
            bitwise_operators,
            shift_operators,
            logical_operators,
            relational_opearators,
            arithmetic_compound_assignment,
            bitwise_compound_assignment,
            shift_compound_assignment,
            assignment_query,
            compound_assignment_query,
            binary_expression_query,
            function_declaration_query,
            struct_declaration_query,
            get_binary_expression_operator,
            get_function_declaration,
            get_struct_declaration,
            get_if_declaration,
            if_declaration_query
        )

    @property
    def get_if_query(self):
        return self._get_if_query