from abc import ABC
from ts import (
    Node,
)
from .type import *
from .c_symbol_table import CSymbolTable
from .tree import Tree

class SymbolTableFiller(ABC):
    def fill(self, root: Node) -> Tree[CSymbolTable]:
        pass