from abc import ABC, abstractmethod
from ts import Node
from .cfa import CFA
from .cfa_node import CFANode

class CFAFactory(ABC):
    @abstractmethod
    def create(self, root: Node) -> CFA[CFANode]: pass