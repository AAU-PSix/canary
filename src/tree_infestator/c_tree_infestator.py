from typing import List, Dict, Callable
from ts import (
    Node,
    Parser,
    Tree,
    CSyntax,
    CNodeType,
    CField
)
from cfa import CFA
from .c_canary_factory import CCanaryFactory
from .tree_infection import TreeInfection
from .tree_infestator import TreeInfestator

class CTreeInfestator(TreeInfestator):
    def __init__(self, parser: Parser, canary_factory: CCanaryFactory) -> None:
        self._parser = parser
        self._canary_factory = canary_factory
        self._syntax = CSyntax()
        super().__init__()

    def immediate_structure_descendent(self, node: Node) -> Node:
        return self._syntax.get_immediate_structure_descendent(node)

    def nests_of_if_condition(self, condition: Node) -> List[Node]:
        # The parent of the condition is the "if_statement" itself.
        return [ condition.parent ]

    def nests_of_while_condition(self, condition: Node) -> List[Node]:
        # We take the parent because the node for a "while"-loop
        #   will always be of type "parenthesized_expression"
        #   as the immediate "child" of the "while_statement"
        return [ condition.parent ]

    def nests_of_do_while_condition(self, condition: Node) -> List[Node]:
        # We take the parent because the node for a "do while"-loop
        #   will always be of type "parenthesized_expression"
        #   as the immediate "child" of the "while_statement"
        return [ condition.parent ]

    def nests_of_for_loop_body(self, body: Node) -> List[Node]:
        return [ body.parent ]

    def nests_of_case_value_for_switch(self, condition: Node) -> List[Node]:
        # The parent of a switch condition is the condition itself
        return [ condition.parent ]

    def nests_of_labeled_statement(self, label: Node) -> List[Node]:
        return [ label ]

    def nests_of_expression_statement(self, expression_stmt: Node) -> List[Node]:
        return [ expression_stmt ]

    def nests_declaration(self, declaration: Node) -> List[Node]:
        return [ declaration ]

    def nests(self, cfa: CFA) -> List[Node]:
        nests: List[Node] = list()
        for cfa_node in cfa.nodes:
            node: Node = cfa_node.node
            # Case 1: if-statements (Including "else if" and "else")
            if self._syntax.is_condition_of_if(node):
                nests.extend(self.nests_of_if_condition(node))
            # Case 2: while-loops
            elif self._syntax.is_condition_of_while(node):
                nests.extend(self.nests_of_while_condition(node))
            # Case 3: do-while-loops
            elif self._syntax.is_condition_of_do_while(node):
                nests.extend(self.nests_of_do_while_condition(node))
            # Case 4: for-loop
            # Since a for-loop can exist without a "init", "cond", and "update"
            #   The only persistent aspect of it is the body, which is always included.
            elif self._syntax.is_body_of_for_loop(node):
                nests.extend(self.nests_of_for_loop_body(node))
            # Case 5: Switch (Cases and default)
            elif self._syntax.is_condition_of_switch(node):
                nests.extend(self.nests_of_case_value_for_switch(node))
            # Case 6: Labels
            elif self._syntax.is_labeled_statement(node):
                nests.extend(self.nests_of_labeled_statement(node))
            # Case 7: Expression statement
            elif self._syntax.is_expression_statement(node):
                nests.extend(self.nests_of_expression_statement(node))
            # Case 8: Declaration
            elif self._syntax.is_declaration(node):
                nests.extend(self.nests_declaration(node))
        return nests

    def infection_spore_for_expression_statement(self, node: Node) -> List[TreeInfection]:
        return [ self._canary_factory.append_state_tweet(node) ]

    def infection_spore_for_declaration(self, node: Node) -> List[TreeInfection]:
        return [ self._canary_factory.append_location_tweet(node) ]

    def infection_spore_if_statement(self, if_stmt: Node) -> List[TreeInfection]:
        infections: List[TreeInfection] = [ ]
        # We dont have to check if "consequence" is None, because every
        #   "if_statement" has a consequence of its "condition"
        consequence: Node = if_stmt.child_by_field(CField.CONSEQUENCE)
        infections.extend(self._canary_factory.create_location_tweets(consequence))

        # If it is an "else if", then it is handled as a seperate "if"
        alternative: Node = if_stmt.child_by_field(CField.ALTERNATIVE)
        if alternative is not None and not self._syntax.is_else_if(if_stmt):
            infections.extend(self._canary_factory.create_location_tweets(alternative))
        return infections

    def infection_spore_while_statement(self, while_stmt: Node) -> List[TreeInfection]:
        body: Node = while_stmt.child_by_field(CField.BODY)
        return self._canary_factory.create_location_tweets(body)

    def infection_spore_do_statement(self, do_stmt: Node) -> List[TreeInfection]:
        body: Node = do_stmt.child_by_field(CField.BODY)
        return self._canary_factory.create_location_tweets(body)

    def infection_spore_for_statement(self, for_stmt: Node) -> List[TreeInfection]:
        body: Node = self._syntax.get_for_loop_body(for_stmt)
        return self._canary_factory.create_location_tweets(body)

    def infection_spore_switch_statement(self, switch_stmt: Node) -> List[TreeInfection]:
        infections: List[TreeInfection] = [ ]
        body: Node = switch_stmt.child_by_field(CField.BODY)
        for case in body.named_children:
            is_default: bool = self._syntax.is_default_switch_case(case)
            if is_default:
                infections.append(
                    # The second (index 1) child is the ":" character for default cases
                    self._canary_factory.append_location_tweet(case.children[1])
                )
            else:
                infections.append(
                    # The second (index 1) child is the ":" character for normal cases
                    self._canary_factory.append_location_tweet(case.children[2])
                )
        return infections

    def infection_spore_labeled_statement(self, node: Node) -> List[TreeInfection]:
        # For a "labeled_statement" the second child (index 1) is the ":"
        return [ self._canary_factory.append_location_tweet(node.children[1]) ]

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        probes: Dict[str, Callable[[Node], List[TreeInfection]]] = {
            # Sequential statements
            CNodeType.EXPRESSION_STATEMENT.value: self.infection_spore_for_expression_statement,
            CNodeType.DECLARATION.value: self.infection_spore_for_declaration,
            # Control structures
            CNodeType.IF_STATEMENT.value: self.infection_spore_if_statement,
            CNodeType.WHILE_STATEMENT.value: self.infection_spore_while_statement,
            CNodeType.DO_STATEMENT.value: self.infection_spore_do_statement,
            CNodeType.FOR_STATEMENT.value: self.infection_spore_for_statement,
            CNodeType.SWITCH_STATEMENT.value: self.infection_spore_switch_statement,
            # Unconditional jump
            CNodeType.LABELED_STATEMENT.value: self.infection_spore_labeled_statement,
        }

        # Step 1: Find the infections
        infections: List[TreeInfection] = [ ]
        for nest in self.nests(cfa):
            if nest.type in probes:
                infections.extend(probes[nest.type](nest))

        # Step 2: Infect the tree from end to start
        infections.sort(key=lambda x: x.last_byte_index, reverse=True)
        for infection in infections:
            tree = infection.do(self._parser, tree)

        return tree