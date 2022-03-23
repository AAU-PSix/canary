from src.ts import *
from src.cfa import *

class TreeInfestator:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def is_condition_of_if(self, node: Node) -> bool:
        if_statement: Node = node.parent
        if if_statement is None or if_statement.type != "if_statement":
            return False
        condition: Node = if_statement.child_by_field_name("condition")
        return condition is not None and node == condition

    def nests_of_if_condition(self, condition: Node) -> List[Node]:
        nests: List[Node] = list()
        if_statement: Node = condition.parent
        consequence: Node = if_statement.child_by_field_name("consequence")
        if consequence is not None: nests.append(consequence)
        alternative: Node = if_statement.child_by_field_name("alternative")
        if alternative is not None: nests.append(alternative)
        return nests

    def is_condition_of_while(self, node: Node) -> bool:
        while_statement: Node = node.parent
        if while_statement is None or while_statement.type != "while_statement":
            return False
        condition: Node = while_statement.child_by_field_name("condition")
        return condition is not None and node == condition

    def nests_of_while_condition(self, condition: Node) -> List[Node]:
        # We take the parent because the node for a "while"-loop
        #   will always be of type "parenthesized_expression"
        #   as the immediate "child" of the "while_statement"
        # TODO: Assumes that the body is always a block.
        while_statement: Node = condition.parent
        return [ while_statement.child_by_field_name("body") ]

    def is_condition_of_do_while(self, node: Node) -> bool:
        do_while_statement: Node = node.parent
        if do_while_statement is None or do_while_statement.type != "do_statement":
            return False
        condition: Node = do_while_statement.child_by_field_name("condition")
        return condition is not None and node == condition

    def nests_of_do_while_condition(self, condition: Node) -> List[Node]:
        # We take the parent because the node for a "do while"-loop
        #   will always be of type "parenthesized_expression"
        #   as the immediate "child" of the "while_statement"
        # TODO: Assumes that the body is always a block.
        while_statement: Node = condition.parent
        return [ while_statement.child_by_field_name("body") ]

    def nests(self, cfa: CFA) -> List[Node]:
        nests: List[Node] = list()
        for cfa_node in cfa.nodes:
            node: Node = cfa_node.node
            # Case 1: if-statements (Including "else if" and "else")
            if self.is_condition_of_if(node):
                nests.extend(self.nests_of_if_condition(node))
            # Case 2: while-loops
            elif self.is_condition_of_while(node):
                nests.extend(self.nests_of_while_condition(node))
            # Case 3: do-while-loops
            elif self.is_condition_of_do_while(node):
                nests.extend(self.nests_of_do_while_condition(node))
        nests.sort(key=lambda x: x.start_byte, reverse=True)
        return nests

    def infect_compound_statement(self, tree: Tree, node: Node) -> Tree:
        # For a "compound_statement" the "child 0" will alwaysbe the "{"
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