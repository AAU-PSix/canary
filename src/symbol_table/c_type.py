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

class CSymbolTable(LexicalSymbolTable):
    def __init__(
        self,
        parent: "LexicalSymbolTable" = None,
        children: List["LexicalSymbolTable"] = list()
    ) -> None:
        super().__init__(parent, children)

    # We have to override the original to support shadowing
    def enter(self, identifier: str, type: Type, lexical_index: int) -> bool:
        declaration = LexicalDeclaration(identifier, type, lexical_index)
        self._declarations.append(declaration)
        return True

    def identifiers(self, index: int = None) -> List[str]:
        identifiers = self.local_identifiers(index)

        for table in self.lexical_traversal():
            if table is self: continue
            for declaration in table._declarations:
                if declaration.lexical_index < self.last_lexical_index:
                    identifiers.append(declaration.identifier)
                # Compilers for C allows "implicit declaration of function"
                #   Which means that "functions" can be used before they are declared.
                elif isinstance(declaration.type, SubroutineType):
                    identifiers.append(declaration.identifier)
        return identifiers