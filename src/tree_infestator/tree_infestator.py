from src.ts import *
from src.cfa import *

class TreeInfestator:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def is_condition_of_if(self, node: Node) -> bool:
        if_statement: Node = node.parent
        condition: Node = if_statement.child_by_field_name("condition")
        return condition is not None and node == condition

    def nests_of_if_statement(self, condition: Node) -> List[Node]:
        nests: List[Node] = list()
        if_statement: Node = condition.parent
        consequence: Node = if_statement.child_by_field_name("consequence")
        if consequence is not None: nests.append(consequence)
        alternative: Node = if_statement.child_by_field_name("alternative")
        if alternative is not None: nests.append(alternative)
        return nests

    def nests(self, cfa: CFA) -> List[Node]:
        nests: List[Node] = list()
        for cfa_node in cfa.nodes:
            node: Node = cfa_node.node
            if self.is_condition_of_if(node):
                nests.extend(self.nests_of_if_statement(node))
        nests.sort(key=lambda x: x.start_byte, reverse=True)
        return nests

    def infect_compound_statement(self, tree: Tree, node: Node) -> Tree:
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect_expression_statement(self, tree: Tree, node: Node) -> Tree:
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect_declaration(self, tree: Tree, node: Node) -> Tree:
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        infections: Dict[str, Callable[[Tree, Node], Tree]] = {
            "compound_statement": self.infect_compound_statement,
            "expression_statement": self.infect_expression_statement,
            "declaration": self.infect_declaration,
        }
        nests: List[Node] = self.nests(cfa)
        for nest in nests:
            if nest.type in infections:
                tree = infections[nest.type](tree, nest)
        return tree