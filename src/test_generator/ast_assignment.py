from typing import Any
from .ast_expression_statement import ExpressionStatement
from .ast_expression import Expression
from .ast_statement import Statement

class Assignment(Statement):
    def __init__(self, lhs: str, rhs: ExpressionStatement = None) -> None:
        self._lhs = lhs
        self._rhs = rhs

    @property
    def lhs(self) -> str:
        return self._lhs

    @property
    def rhs(self) -> Expression:
        return self._rhs

    def accept(self, visitor: Any):
        visitor.visit_assignment(self)