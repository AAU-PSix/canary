from typing import Any
from .ast_statement import Statement
from .ast_expression import Expression

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression) -> None:
        self._expression = expression
        super().__init__()

    @property
    def epxression(self) -> Expression:
        return self._expression

    def accept(self, visitor: Any):
        visitor.visit_expression_statement(self)