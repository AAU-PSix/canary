from ts import Node

class CFANode:
    def __init__(self, node: Node) -> None:
        self.node = node

    def __str__(self) -> str:
        return f'[{self.node.start_byte}, {self.node.end_byte}] {self.node.type}'