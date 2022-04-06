from typing import Any
from .ast_statement import Statement
from .ast_expression import Expression

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

    def accept(self, visitor: Any):
        visitor.visit_declaration(self)