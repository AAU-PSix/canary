from abc import ABC, abstractmethod
from ts import Tree
from cfa import (
    CFA,
    CFANode
)

class TreeInfestator(ABC):
    @abstractmethod
    def infect(self, tree: Tree, cfa: CFA[CFANode]) -> Tree:
        pass