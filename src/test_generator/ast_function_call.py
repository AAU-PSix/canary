from typing import List
from typing import Any
from .ast_expression import Expression

class FunctionCall(Expression):
    def __init__(self, name: str, actual_parameters: List[Expression] = list()) -> None:
        self._name = name
        self._actual_parameters = actual_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def actual_parameters(self) -> "List[Expression]":
        return self._actual_parameters

    def accept(self, visitor: Any):
        visitor.visit_function_call(self)