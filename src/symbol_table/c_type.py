from enum import Enum
from symtable import SymbolTable
from typing import Dict
from ts import (
    Node,
    CField,
    Tree
)
from symbol_table import (
    LexicalDeclaration,
    LexicalSymbolTabelBuilder,
    LexicalSymbolTable
)
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

class CTypeFactory():
    def __init__(self) -> None:
        self._primitives: Dict[str, PrimitiveType] = {
            "int": PrimitiveType("int")
        }
    
    def create_primitive_type(
        self,
        tree: Tree,
        node: Node
    ) -> PrimitiveType:
        return self._primitives[tree.contents_of(node)]

    def create_subroutine_type(
        self,
        tree: Tree,
        function_definition: Node
    ) -> SubroutineType[LexicalDeclaration]:
        return_type_node = function_definition.child_by_field(CField.TYPE)
        declarator_node = function_definition.child_by_field(CField.DECLARATOR)
        parameters_node = declarator_node.child_by_field(CField.PARAMETERS)
        return_type = self.create_primitive_type(tree, return_type_node)

        parameters: List[LexicalDeclaration] = [ ]
        for parameter_node in parameters_node.named_children:
            parameter_type_node = parameter_node.child_by_field(CField.TYPE)
            parameter_type = self.create_primitive_type(tree, parameter_type_node)
            parameter_identifier_node = parameter_node.child_by_field(CField.DECLARATOR)
            parameter_identifier = tree.contents_of(parameter_identifier_node)
            parameter_declaration = LexicalDeclaration(
                parameter_identifier,
                parameter_type,
                parameter_node.end_byte,
            )
            parameters.append(parameter_declaration)
        function_type = SubroutineType(return_type, parameters)

        return function_type

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
