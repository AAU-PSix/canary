from src.ts import *
from src.cfa import *

class TreeInfection:
    def __init__(self, node: Node, nest: str) -> None:
        self._node = node
        self._nest = nest

    def do(self, parser: Parser, tree: Tree) -> Tree:
        return parser.append(tree, self.node, self.nest)

    @property
    def node(self) -> Node:
        return self._node

    @property
    def nest(self) -> str:
        return self._nest

    def __eq__(self, other: "TreeInfection") -> bool:
        if other is None: return False
        return self.node == other.node and \
            self.nest == other.nest

    def __ne__(self, other: "TreeInfection") -> bool:
        return not (self == other)

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
        # The parent of the condition is the "if_statement" itself.
        return [ condition.parent ]

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
        return [ condition.parent ]

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
        return [ condition.parent ]

    def is_body_of_for_loop(self, node: Node) -> bool:
        for_statement: Node = node.parent
        if for_statement is None or for_statement.type != "for_statement":
            return False
        body: Node = for_statement.named_children[-1]
        return body is not None and node == body

    def nests_of_for_loop_body(self, body: Node) -> List[Node]:
        return [ body.parent ]

    def is_condition_of_switch(self, node: Node) -> bool:
        switch_stmt: Node = node.parent
        if switch_stmt is None or switch_stmt.type != "switch_statement":
            return False
        condition: Node = switch_stmt.child_by_field_name("condition")
        return condition is not None and node == condition
    
    def nests_of_case_value_for_switch(self, condition: Node) -> List[Node]:
        # The parent of a switch condition is the condition itself
        return [ condition.parent ]

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
            # Since a for-loop can exist without a "init", "cond", and "update"
            #   The only persistent aspect of it is the body, which is always included.
            elif self.is_body_of_for_loop(node):
                nests.extend(self.nests_of_for_loop_body(node))
            # Case 5: Switch (Cases and default)
            elif self.is_condition_of_switch(node):
                nests.extend(self.nests_of_case_value_for_switch(node))
            # Case 6: Labels
            elif self.is_labeled_statement(node):
                nests.extend(self.nests_of_labeled_statement(node))
        return nests

    def infection_spore_for_expression_statement(self, node: Node) -> List[TreeInfection]:
        return [ TreeInfection(node.children[0], "TWEET();") ]

    def infection_spore_for_declaration(self, node: Node) -> List[TreeInfection]:
        return [ TreeInfection(node.children[0], "TWEET();") ]

    def infection_spore_if_statement(self, if_stmt: Node) -> List[TreeInfection]:
        infections: List[TreeInfection] = [ ]
        consequence: Node = if_stmt.child_by_field_name("consequence")
        if consequence is not None:
            infections.append(TreeInfection(consequence.children[0], "TWEET();"))

        alternative: Node = if_stmt.child_by_field_name("alternative")
        # If the alternative is a "if_statement" then it is an "else if(...)"
        if alternative is not None and alternative.type != "if_statement":
            infections.append(TreeInfection(alternative.children[0], "TWEET();"))
        return infections

    def infection_spore_while_statement(self, while_stmt: Node) -> List[TreeInfection]:
        body: Node = while_stmt.child_by_field_name("body")
        return [ TreeInfection(body.children[0], "TWEET();") ]

    def infection_spore_do_statement(self, do_stmt: Node) -> List[TreeInfection]:
        body: Node = do_stmt.child_by_field_name("body")
        return [ TreeInfection(body.children[0], "TWEET();") ]

    def infection_spore_for_statement(self, for_stmt: Node) -> List[TreeInfection]:
        body: Node = for_stmt.named_children[-1]
        return [ TreeInfection(body.children[0], "TWEET();") ]

    def infection_spore_switch_statement(self, switch_stmt: Node) -> List[TreeInfection]:
        infections: List[TreeInfection] = [ ]
        body: Node = switch_stmt.child_by_field_name("body")
        if body is None: return [ ]
        for case in body.named_children:
            is_default: bool = case.child_by_field_name("value") is None
            if is_default:
                infections.append(TreeInfection(case.children[1], "TWEET();"))
            else:
                infections.append(TreeInfection(case.children[2], "TWEET();"))
        return infections

    def infection_spore_labeled_statement(self, node: Node) -> List[TreeInfection]:
        # For a "labeled_statement" the second child (index 1) is the ":"
        return [ TreeInfection(node.children[1], "TWEET();") ]

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        probes: Dict[str, Callable[[Node], List[TreeInfection]]] = {
            # Sequential statements
            "expression_statement": self.infection_spore_for_expression_statement,
            "declaration": self.infection_spore_for_declaration,
            # Control structures
            "if_statement": self.infection_spore_if_statement,
            "while_statement": self.infection_spore_while_statement,
            "do_statement": self.infection_spore_do_statement,
            "for_statement": self.infection_spore_for_statement,
            "switch_statement": self.infection_spore_switch_statement,
            # Unconditional jump
            "labeled_statement": self.infection_spore_labeled_statement,
        }

        # Step 1: Find the infections
        infections: List[TreeInfection] = [ ]
        for nest in self.nests(cfa):
            if nest.type in probes:
                infections.extend(probes[nest.type](nest))

        # Step 2: Infect the tree from end to start
        infections.sort(key=lambda x: x.node.start_byte, reverse=True)
        for infection in infections:
            tree = infection.do(self._parser, tree)

        return tree