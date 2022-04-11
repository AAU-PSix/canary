from typing import Generic
from .cfa_node import CFANode
from .t_cfa_node import TCFANode

class CFAEdge(Generic[TCFANode]):
    def __init__(self, source: TCFANode, destination: TCFANode, label: str = None) -> None:
        self.source = source
        self.destination = destination
        self.label = label