from src.ts import *
from src.cfa import *

class TreeInfestator:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def is_condition_of_if(self, node: Node) -> bool:
        if_statement: Node = node.parent
        alternative: Node = if_statement.child_by_field_name("condition")
        return alternative is not None and node == alternative

    def is_consequence_of_if(self, node: Node) -> bool:
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

    def is_branch(self, node: Node) -> bool:
        return self.is_consequence_of_if(node) or \
            self.is_alternative_of_if(node)

    def sorted_cfa(self, cfa: CFA) -> List[CFANode]:
        nodes: List[CFANode] = list(cfa.breadth_first_traverse())
        nodes.sort(key=lambda x: x.node.end_byte, reverse=True)
        return nodes

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        cfa_nodes: List[CFANode] = self.sorted_cfa(cfa)
        for cfa_node in cfa_nodes:
            if self.is_alternative_of_if(cfa_node.node):
                tree = self._parser.append(tree, cfa_node.node, "TWEET();")
            elif self.is_condition_of_if(cfa_node.node):
                tree = self._parser.append(tree, cfa_node.node, "TWEET();")
        return tree