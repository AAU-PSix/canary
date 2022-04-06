from typing import Any
from .ast_node import ASTNode

class Expression(ASTNode):
    def __init__(self) -> None:
        pass

    def accept(self, visitor: Any):
        visitor.visit_expression(self)