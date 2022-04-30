from typing import Iterable, List
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
    ARITHMETIC_ADDITION_ADDITION = "++"
    ARITHMETIC_SUBTRACTION_SUBTRACTION = "--"
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
    Logical_NOT = "!"
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
    # Types
    PRIMITIVE_TYPE = "primitive_type"
    SIZED_TYPE_SPECIFIER = "sized_type_specifier"
    STRUCT_SPECIFIER = "struct_specifier"
    UNION_SPECIFIER = "union_specifier"
    # Constructs
    EXPRESSION_STATEMENT = "expression_statement"
    ASSIGNMENT_EXPRESSION = "assignment_expression"
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
    FUNCTION_DEFINITION = "function_definition"
    TYPE_DEFINITION = "type_definition"
    ENUM_SPECIFIER = "enum_specifier"
    STORAGE_CLASS_SPECIFIERS = "storage_class_specifier"
    TYPE_QUALIFIER = "type_qualifier"
    INIT_DECLARATOR = "init_declarator"
    ARRAY_DECLARATOR = "array_declarator"
    POINTER_DECLARATOR = "pointer_declarator"
    PARAMETER_DECLARATION = "parameter_declaration"
    PREPROC_IFDEF = "preproc_ifdef"
    PREPROC_DEF = "preproc_def"
    CASE_STATEMENT = "case_statement"
    PARENTHESIZED_EXPRESSION = "parenthesized_expression"
    UNARY_EXPRESSION = "unary_expression"
    BINARY_EXPRESSION = "binary_expression"
    NUMBER_LITERAL = "number_literal"
    UPDATE_EXPRESSION = "update_expression"

class CSyntax(Syntax):
    @property
    def plain_assignment(self) -> Iterable[CNodeType]:
        return [
            CNodeType.PLAIN_ASSIGNMENT,
        ]

    @property
    def logical_unary_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.Logical_NOT
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
    def arithmetic_unary_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.ARITHMETIC_ADDITION,
            CNodeType.ARITHMETIC_SUBTRACTION,
        ]

    @property
    def update_expression_operators(self) -> Iterable[CNodeType]:
        return [
            CNodeType.ARITHMETIC_ADDITION_ADDITION,
            CNodeType.ARITHMETIC_SUBTRACTION_SUBTRACTION,
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
    def relational_operators(self) -> Iterable[CNodeType]:
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
    def structures(self) -> Iterable[CNodeType]:
        return [
            CNodeType.IF_STATEMENT,
            CNodeType.WHILE_STATEMENT,
            CNodeType.DO_STATEMENT,
            CNodeType.FOR_STATEMENT,
            CNodeType.SWITCH_STATEMENT,
            CNodeType.FUNCTION_DEFINITION
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
    def unary_expression_query(self) -> str:
        return '((unary_expression) @exp)'

    @property
    def update_expression_query(self) -> str:
        return '((update_expression) @exp)'

    @property
    def number_literal_query(self) -> str:
        return '((number_literal) @num)'

    @property
    def function_declaration_query(self) -> str:
        return "((function_definition) @def)"

    @property
    def struct_declaration_query(self) -> str:
        return '((struct_specifier) @spec)'

    @property
    def if_statement_query(self) -> str:
        return '(if_statement) @if'

    @property
    def declaration_query(self) -> str:
        return '(declaration) @declaration'

    def get_binary_expression_operator(self, node: Node) -> Node:
        return node.children[1]

    def get_function_definitions(self, node: Node) -> Node:
        return node

    def get_struct_declaration(self, node: Node) -> Node:
        return node

    def get_if_declaration(self, node: Node) -> Node:
        return node

    def get_for_loop_body(self, node: Node) -> Node:
        return node.named_children[-1]

    def get_function_identifier(self, definition: Node) -> Node:
        current = definition \
            .child_by_field(CField.DECLARATOR) \
            .child_by_field(CField.DECLARATOR)
        if current is None: return None
        while True:
            next = current.child_by_field(CField.DECLARATOR)
            if next is None: break
            current = next
        return current

    def get_immediate_structure_descendent(self, node: Node) -> Node:
        if node is None: return None
        types: List[str] = [ nodeType.value for nodeType in self.structures ]
        return node.get_immediate_descendent_of_types(types)

    def get_structure_descendent(self, node: Node) -> Node:
        if node is None: return None
        types: List[str] = [ nodeType.value for nodeType in self.structures ]
        return node.get_descendent_of_types(types)

    def is_immediate_structure_descendent(self, node: Node, type: CNodeType) -> bool:
        if node is None: return False
        immediate_structure: Node = self.get_immediate_structure_descendent(node)
        if immediate_structure is None: return False
        immediate_type: CNodeType = self.node_field(immediate_structure.type)
        return type is immediate_type

    def is_structure_descendent(self, node: Node, type: CNodeType) -> bool:
        if node is None: return False
        immediate_structure: Node = self.get_structure_descendent(node)
        if immediate_structure is None: return False
        immediate_type: CNodeType = self.node_field(immediate_structure.type)
        return type is immediate_type

    def is_default_switch_case(self, case: Node) -> bool:
        if case is None: return False
        return case.child_by_field(CField.VALUE) is None

    def is_empty_switch_case(self, case: Node) -> bool:
        if case is None: return False
        if self.is_default_switch_case(case):
            return case.named_child_count < 1
        return case.named_child_count == 1

    def is_switch_case(self, case: Node) -> bool:
        if not case.parent.is_type(CNodeType.CASE_STATEMENT):
            return False
        return case.parent.child_by_field(CField.VALUE) == case

    def is_field_of_type(self, node: Node, structure: CNodeType, field: CField) -> bool:
        if node is None: return False
        structure_node: Node = self.get_structure_descendent(node)
        if structure_node is None or not structure_node.is_type(structure):
            return False
        field_node: Node = structure_node.child_by_field(field)
        return field is not None and node == field_node

    def is_condition_of_if(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.IF_STATEMENT, CField.CONDITION
        )

    def is_condition_of_while(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.WHILE_STATEMENT, CField.CONDITION
        )
        
    def is_condition_of_for(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.FOR_STATEMENT, CField.CONDITION
        )

    def is_initialisation_of_for(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.FOR_STATEMENT, CField.INITIALIZER
        )

    def is_update_of_for(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.FOR_STATEMENT, CField.UPDATE
        )

    def is_condition_of_do_while(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.DO_STATEMENT, CField.CONDITION
        )

    def is_body_of_for_loop(self, node: Node) -> bool:
        # A for-loop does not have the "body" as a field.
        #   for this reason we just have to check if the for-loop
        #   is the first descendent of the structure.
        for_statement: Node = node.get_immediate_descendent_of_types(
            [ CNodeType.FOR_STATEMENT.value ]
        )
        if for_statement is None: return False

        # The last named child of the for_statement node is the body of the loop
        for_body = self.get_for_loop_body(for_statement)
        return for_body == node or \
            node.is_immediate_descendent_of_node(for_body)

    def is_condition_of_switch(self, node: Node) -> bool:
        return self.is_field_of_type(
            node, CNodeType.SWITCH_STATEMENT, CField.CONDITION
        )

    def has_else_if(self, node: Node) -> bool:
        alternative: Node = node.child_by_field(CField.ALTERNATIVE)
        return alternative is not None and alternative.is_type(CNodeType.IF_STATEMENT)

    def is_labeled_statement(self, node: Node) -> bool:
        return node is not None and node.is_type(CNodeType.LABELED_STATEMENT)

    def is_expression_statement(self, node: Node) -> bool:
        return node is not None and node.is_type(CNodeType.EXPRESSION_STATEMENT)

    def is_return_statement(self, node: Node) -> bool:
        return node is not None and node.is_type(CNodeType.RETURN_STATEMENT)

    def is_declaration(self, node: Node) -> bool:
        return node is not None and node.is_type(CNodeType.DECLARATION)

    def is_immediate_of_function_definition(self, node: Node) -> bool:
        return node is not None and node.get_immediate_descendent_of_types_field(
            [ CNodeType.FUNCTION_DEFINITION.value ], CField.BODY
        ) is not None

    def is_immediate_of_translation_unit(self, node: Node) -> bool:
        return node is not None and node.get_immediate_descendent_of_types(
            [ CNodeType.TRANSLATION_UNIT ]
        ) is not None

    def is_goto_statement(self, node: Node) -> bool:
        return node is not None and node.is_type(CNodeType.GOTO_STATEMENT)

    def node_field(self, node_type: str) -> CNodeType:
        return CNodeType(node_type)