from ts import Node
from .cfa_node import CFANode

class LocalisedNode(CFANode):
    def __init__(self, node: Node, location: str = None) -> None:
        self.location: str = location
        super().__init__(node)

    def __str__(self) -> str:
        return f'loc. {self.location}\n[{self.node.start_byte}, {self.node.end_byte}] {self.node.type}'
