from abc import ABC, abstractmethod
from cfa import NodeType, Node, CFAEdge, CFAGeneric, CFA
from cfa.c_cfa_factory import CCFAFactory

class DecoratedNode(Node):
    def __init__(self, node: Node) -> None:
        self.location = -99
        super().__init__(node)

class LocalisedCFA(CFAGeneric[DecoratedNode, CFAEdge]):
    pass

class LocalisedCFACFactory(CCFAFactory):
    pass

class CFADecorator(ABC):
    def __init__(self, cfa:CFA) -> None:
        self.cfa = cfa
        super().__init__()

    @abstractmethod
    def decorate() -> CFA:
        pass

class LocationDecorator(CFADecorator):
    def __init__(self, CFA: CFA) -> None:
        self.cfa = CFA

    def decorate(a:LocalisedCFA) -> LocalisedCFA:
        pass
    

    