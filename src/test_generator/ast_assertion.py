from typing import Any
from .ast_expression import Expression

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

    def accept(self, visitor: Any):
        visitor.visit_assertion(self)