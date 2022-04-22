from ts import Node
from .cfa_node import CFANode

class LocalisedNode(CFANode):
    def __init__(self, node: Node, location: str = None) -> None:
        self.location: str = location
        super().__init__(node)

    def __str__(self) -> str:
        text = f'loc. {self.location}\n[{self.node.start_byte}, {self.node.end_byte}] {self.node.type}'
        if hasattr(self, "amount_killed") and hasattr(self, "amount_survived"):
            total_mutations = self.amount_survived + self.amount_killed
            if total_mutations > 0:
                mutation_score = self.amount_killed / total_mutations
                text += f"\n{self.amount_killed} killed/{total_mutations} total={mutation_score}\n"
        return text
