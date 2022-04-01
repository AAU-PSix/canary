from symbol_table import SymbolTable
from .type import *

class PointerType(Type):
    def __init__(self, multiple_indirection: int, type: Type) -> None:
        self._multiple_indirection = multiple_indirection
        super().__init__(type.identifier)

    @property
    def multiple_indirection(self) -> int:
        return self._multiple_indirection

class CSymbolTable(SymbolTable):
    def __init__(
        self,
        parent: "SymbolTable" = None,
        children: List["SymbolTable"] = list()
    ) -> None:
        super().__init__(parent, children)

    def enter(self, type: Type) -> bool:
        self._declarations[type.identifier] = type

    def enter_extern(self, type: Type) -> "CSymbolTable":
        return self