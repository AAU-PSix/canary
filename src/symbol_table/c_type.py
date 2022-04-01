from enum import Enum
from symbol_table import SymbolTable
from .type import *

class CTypeQualifier(Enum):
    CONST = "const",
    VOLATILE = "volatile",
    RESTRICT = "restrict",
    ATOMIC = "_Atomic",
    STATIC = "static"

class CType(Type):
    def __init__(
        self,
        type: Type,
        qualifiers: List[CTypeQualifier]
    ) -> None:
        self._qualifiers = qualifiers
        super().__init__(type.identifier)

    @property
    def qualifier(self) -> List[CTypeQualifier]:
        return self._qualifiers

class CPrimitiveType(CType, PrimitiveType): pass

class PointerType(CType):
    def __init__(self, multiple_indirection: int, type: Type) -> None:
        self._multiple_indirection = multiple_indirection
        super().__init__(type.identifier)

    @property
    def multiple_indirection(self) -> int:
        return self._multiple_indirection

class CSubroutineType(CType, SubroutineType): pass

class CTypeStruct(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)

class CUnionType(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)

class CSymbolTable(SymbolTable):
    def __init__(
        self,
        parent: "SymbolTable" = None,
        children: List["SymbolTable"] = list()
    ) -> None:
        super().__init__(parent, children)

    # We have to override the original to support shadowing
    def enter(self, type: Type) -> bool:
        self._declarations[type.identifier] = type