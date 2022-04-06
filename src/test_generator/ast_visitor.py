from abc import ABC, abstractmethod

from .ast_expression import Expression
from .ast_statement import Statement
from .ast_expression_statement import ExpressionStatement
from .ast_constant import Constant
from .ast_assignment import Assignment
from .ast_declaration import Declaration
from .ast_function_call import FunctionCall
from .ast_assertion import Assertion

class ASTVisitor(ABC):
    @abstractmethod
    def visit_expression(self, expression: Expression): pass
    @abstractmethod
    def visit_statement(self, statement: Statement): pass
    @abstractmethod
    def visit_expression_statement(self, statement: ExpressionStatement): pass
    @abstractmethod
    def visit_assertion(self, assertion: Assertion): pass
    @abstractmethod
    def visit_constant(self, constant: Constant): pass
    @abstractmethod
    def visit_assignment(self, assignment: Assignment): pass
    @abstractmethod
    def visit_declaration(self, assignment: Declaration): pass
    @abstractmethod
    def visit_function_call(self, function_call: FunctionCall): pass