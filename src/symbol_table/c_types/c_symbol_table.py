from typing import List
from ..lexical_symbol_table_builder import LexicalSymbolTable
from ..types.subroutine_type import SubroutineType
from ..lexical_declaration import LexicalDeclaration

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