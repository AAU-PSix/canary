from .cfa import CFA
from .cfa_node import CFANode
from ts import Node

class LocalisedNode(CFANode):
    def __init__(self, node: Node, location: str = None) -> None:
        self.location: str = location
        super().__init__(node)

    def __str__(self) -> str:
        return f'loc. {self.location}\n[{self.node.start_byte}, {self.node.end_byte}] {self.node.type}'

class LocalisedCFA(CFA[LocalisedNode]):
    def __init__(self, root: LocalisedNode) -> None:
        super().__init__(root)
