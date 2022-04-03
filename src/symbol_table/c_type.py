from enum import Enum
from symbol_table import LexicalDeclaration, LexicalSymbolTabelBuilder, LexicalSymbolTable
from .type import *
from .tree import Tree

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
        super().__init__(type.name)

    @property
    def qualifier(self) -> List[CTypeQualifier]:
        return self._qualifiers

class CPrimitiveType(CType, PrimitiveType): pass

class PointerType(CType):
    def __init__(self, multiple_indirection: int, type: Type) -> None:
        self._multiple_indirection = multiple_indirection
        super().__init__(type.name)

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

class CSymbolTable(LexicalSymbolTable["CSymbolTable"]):
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: "LexicalSymbolTable" = None,
        children: List["LexicalSymbolTable"] = list()
    ) -> None:
        super().__init__(
            minimum_lexical_index,
            maximum_lexical_index,
            parent,
            children
        )

    def can_be_referenced(self, declaration: LexicalDeclaration, lexical_upper_bound: int) -> bool:
                # Compilers for C allows "implicit declaration of function"
                #   Which means that "functions" can be used before they are declared.
        return super().can_be_referenced(declaration, lexical_upper_bound) or \
            isinstance(declaration.type, SubroutineType)

class CSymbolTableBuilder(LexicalSymbolTabelBuilder[CSymbolTable]):
    def __init__(self, minimum_lexical_index: int, maximum_lexical_index: int) -> None:
        super().__init__(minimum_lexical_index, maximum_lexical_index)

    def _create(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: CSymbolTable = None,
        children: List[CSymbolTable] = list()
    ) -> CSymbolTable:
        return CSymbolTable(
            minimum_lexical_index,
            maximum_lexical_index,
            parent,
            children
        )