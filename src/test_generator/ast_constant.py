from typing import Any
from .ast_expression import Expression

class Constant(Expression):
    def __init__(self, value: str) -> None:
        self._value = value
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    def accept(self, visitor: Any):
        visitor.visit_constant(self)