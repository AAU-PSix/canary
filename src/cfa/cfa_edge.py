from .cfa_node import CFANode

class CFAEdge:
    def __init__(self, source: CFANode, destination: CFANode, label: str = None) -> None:
        self.source = source
        self.destination = destination
        self.label = label