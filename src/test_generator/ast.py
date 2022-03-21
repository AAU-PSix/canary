from ts import Node, Tree
from typing import List
from abc import ABC, abstractmethod

class FormalParameter:
    def __init__(self, identifier: str, type: str) -> None:
        self._identifier = identifier
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def type(self) -> str:
        return self._type

class FunctionDeclaration:
    def __init__(
        self,
        name: str,
        return_type: str,
        formal_parameters: List[FormalParameter]
    ) -> None:
        self._name = name
        self._return_type = return_type
        self._formal_parameters = formal_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def formal_parameters(self) -> List[FormalParameter]:
        return self._formal_parameters

    @staticmethod
    def create_c(tree: Tree, node: Node) -> "FunctionDeclaration":
        return_type_node: Node = node.child_by_field_name("type")
        return_type: str = tree.contents_of(return_type_node)

        formal_parameters: List[FormalParameter] = list()
        declarator_node: Node = node.child_by_field_name("declarator")

        function_name_node: Node = declarator_node.child_by_field_name("declarator")
        function_name: str = tree.contents_of(function_name_node)

        parameter_list: Node = declarator_node.child_by_field_name("parameters")
        for parameter_declaration in parameter_list.named_children:
            parameter_type_node = parameter_declaration.child_by_field_name("type")
            parameter_identifier_node = parameter_declaration.child_by_field_name("declarator")

            formal_type: str = tree.contents_of(parameter_type_node)
            formal_identifier = tree.contents_of(parameter_identifier_node)

            parameter_declarator_node: Node = parameter_declaration.child_by_field_name("declarator")
            while parameter_declarator_node.type == "pointer_declarator":
                formal_type += "*"
                parameter_declarator_node = parameter_declarator_node.named_children[0]

            formal_parameters.append(
                FormalParameter(formal_identifier, formal_type)
            )

        return FunctionDeclaration(
            function_name, return_type, formal_parameters
        )

class ASTVisitor(ABC):
    @abstractmethod
    def visit_expression(self, expression: "Expression"): pass
    @abstractmethod
    def visit_statement(self, statement: "Statement"): pass
    @abstractmethod
    def visit_expression_statement(self, statement: "ExpressionStatement"): pass
    @abstractmethod
    def visit_assertion(self, assertion: "Assertion"): pass
    @abstractmethod
    def visit_constant(self, constant: "Constant"): pass
    @abstractmethod
    def visit_assignment(self, assignment: "Assignment"): pass
    @abstractmethod
    def visit_declaration(self, assignment: "Declaration"): pass
    @abstractmethod
    def visit_function_call(self, function_call: "FunctionCall"): pass

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor): pass

class Statement(ASTNode):
    def __init__(self) -> None:
        pass

    def accept(self, visitor: ASTVisitor):
        visitor.visit_statement(self)

class Expression(ASTNode):
    def __init__(self) -> None:
        pass

    def accept(self, visitor: ASTVisitor):
        visitor.visit_expression(self)

class FunctionCall(Expression):
    def __init__(self, name: str, actual_parameters: "list[Expression]" = list()) -> None:
        self._name = name
        self._actual_parameters = actual_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def actual_parameters(self) -> "list[Expression]":
        return self._actual_parameters

    def accept(self, visitor: ASTVisitor):
        visitor.visit_function_call(self)

class Constant(Expression):
    def __init__(self, value: str) -> None:
        self._value = value
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    def accept(self, visitor: ASTVisitor):
        visitor.visit_constant(self)

class Assignment(Statement):
    def __init__(self, lhs: str, rhs: Expression = None) -> None:
        self._lhs = lhs
        self._rhs = rhs

    @property
    def lhs(self) -> str:
        return self._lhs

    @property
    def rhs(self) -> Expression:
        return self._rhs

    def accept(self, visitor: ASTVisitor):
        visitor.visit_assignment(self)

class Declaration(Statement):
    def __init__(
        self,
        type: str,
        identifier: str,
        initialization: Expression = None
    ) -> None:
        self._type = type
        self._identifier = identifier
        self._initialization = initialization
        super().__init__()

    @property
    def type(self) -> str:
        return self._type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def initialization(self) -> Expression:
        return self._initialization

    def accept(self, visitor: ASTVisitor):
        visitor.visit_declaration(self)

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression) -> None:
        self._expression = expression
        super().__init__()

    @property
    def epxression(self) -> Expression:
        return self._expression

    def accept(self, visitor: ASTVisitor):
        visitor.visit_expression_statement(self)

class Assertion:
    def __init__(self, actual: Expression, expected: Expression) -> None:
        self._actual = actual
        self._expected = expected

    @property
    def actual(self) -> Expression:
        return self._actual

    @property
    def expected(self) -> Expression:
        return self._expected

    def accept(self, visitor: ASTVisitor):
        visitor.visit_assertion(self)

class TestCase:
    def __init__(
        self,
        name: str,
        arrange: List[Statement],
        act: Statement,
        assertions: List[Assertion]
    ) -> None:
        self._name = name
        self._arrange = arrange
        self._act = act
        self._assertions = assertions

    @property
    def name(self) -> str:
        return self._name

    @property
    def arrange(self) -> List[Statement]:
        return self._arrange

    @property
    def act(self) -> Statement:
        return self._act

    @property
    def assertions(self) -> List[Assertion]:
        return self._assertions