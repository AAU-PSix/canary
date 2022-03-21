from src.ts import *
from src.cfa import *

class TreeInfestator:
    def is_condition_of_if(self, node: Node) -> bool:
        if_statement: Node = node.parent
        alternative: Node = if_statement.child_by_field_name("condition")
        return alternative is not None and node == alternative

    def is_consequence_of_if(self, node: Node) -> bool:
        # Assume that all blocks are wrapped in a "compound_statment"
        if_statement: Node = node.parent
        if node.type != "compound_statement":
            if_statement = if_statement.parent
        alternative: Node = if_statement.child_by_field_name("consequence")
        return alternative is not None and node == alternative

    def is_alternative_of_if(self, node: Node) -> bool:
        if_statement: Node = node.parent
        if node.type != "compound_statement":
            if_statement = if_statement.parent
        alternative: Node = if_statement.child_by_field_name("alternative")
        return alternative is not None and node == alternative

    def sorted_cfa(self, cfa: CFA) -> List[CFANode]:
        nodes: List[CFANode] = list(cfa.breadth_first_traverse())
        nodes.sort(key=lambda x: x.node.end_byte, reverse=True)
        return nodes

    def infect(self, cfa: CFA) -> Tree:
        pass