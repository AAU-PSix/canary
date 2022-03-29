from ts import Node

class CFANode:
    def __init__(self, node: Node, location: int = -1) -> None:
        self.node = node
        self.location = location