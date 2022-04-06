from typing import List
from .c_symbol_table import CSymbolTable
from ..lexical_symbol_table_builder import LexicalSymbolTabelBuilder

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