from abc import ABC
from ts import (
    Node,
)
from .c_types import CSymbolTable
from .tree import Tree

class SymbolTableFiller(ABC):
    def fill(self, root: Node) -> Tree[CSymbolTable]:
        pass