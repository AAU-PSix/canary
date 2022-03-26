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

    def is_body_of_for_loop(self, node: Node) -> bool:
        for_statement: Node = node.parent
        if for_statement is None or for_statement.type != "for_statement":
            return False
        body: Node = for_statement.named_children[-1]
        return body is not None and node == body

    def nests_of_for_loop_body(self, body: Node) -> List[Node]:
        return [ body ]

    def is_case_value_of_switch(self, node: Node) -> bool:
        case: Node = node.parent
        if case is None or case.type != "case_statement":
            return False
        value: Node = case.child_by_field_name("value")
        if value is None or value != node:
            return False
        return True
    
    def nests_of_case_value_for_switch(self, case_value: Node) -> List[Node]:
        return [ case_value.parent ]

    def is_labeled_statement(self, node: Node) -> bool:
        return node.type == "labeled_statement"

    def nests_of_labeled_statement(self, label: Node) -> List[Node]:
        return [ label ]

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
            # Case 4: for-loop
            elif self.is_body_of_for_loop(node):
                nests.extend(self.nests_of_for_loop_body(node))
            # Case 5: Switch (Cases and default)
            elif self.is_case_value_of_switch(node):
                nests.extend(self.nests_of_case_value_for_switch(node))
            # Case 6: Labels
            elif self.is_labeled_statement(node):
                nests.extend(self.nests_of_labeled_statement(node))
        nests.sort(key=lambda x: x.start_byte, reverse=True)
        return nests

    def infect_compound_statement(self, tree: Tree, node: Node) -> Tree:
        # For a "compound_statement" the "child 0" will alwaysbe the "{"
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect_expression_statement(self, tree: Tree, node: Node) -> Tree:
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect_declaration(self, tree: Tree, node: Node) -> Tree:
        return self._parser.append(tree, node.children[0], "TWEET();")

    def infect_case_statement(self, tree: Tree, node: Node) -> Tree:
        # For a "case_statement" the third child (index 2) is the ":"
        return self._parser.append(tree, node.children[2], "TWEET();")

    def infect_labeled_statement(self, tree: Tree, node: Node) -> Tree:
        # For a "labeled_statement" the second child (index 1) is the ":"
        return self._parser.append(tree, node.children[1], "TWEET();")

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        infections: Dict[str, Callable[[Tree, Node], Tree]] = {
            "compound_statement": self.infect_compound_statement,
            "expression_statement": self.infect_expression_statement,
            "declaration": self.infect_declaration,
            "case_statement": self.infect_case_statement,
            "labeled_statement": self.infect_labeled_statement,
        }
        nests: List[Node] = self.nests(cfa)
        for nest in nests:
            if nest.type in infections:
                tree = infections[nest.type](tree, nest)
        return tree