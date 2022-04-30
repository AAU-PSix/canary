from typing import List, Dict, Callable
from ts import (
    Node,
    Parser,
    Tree,
    CSyntax,
    CNodeType,
    CField
)
from cfa import (
    CFA,
    CFANode
)
from .c_canary_factory import CCanaryFactory
from .tree_infection import TreeInfection
from .tree_infestator import TreeInfestator

class CTreeInfestator(TreeInfestator):
    def __init__(self, parser: Parser, canary_factory: CCanaryFactory) -> None:
        self._parser = parser
        self._canary_factory = canary_factory
        self._syntax = CSyntax()
        super().__init__()

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
        return [ body.get_immediate_descendent_of_types(
            [ CNodeType.FOR_STATEMENT.value ]
        ) ]

    def nests_of_case_value_for_switch(self, condition: Node) -> List[Node]:
        # The parent of a switch condition is the condition itself
        return [ condition.parent ]

    def nests_of_labeled_statement(self, label: Node) -> List[Node]:
        return [ label, label.named_children[1] ]

    def nests_of_expression_statement(self, expression_stmt: Node) -> List[Node]:
        return [ expression_stmt ]

    def nests_of_return_statement(self, return_stmt: Node) -> List[Node]:
        return [ return_stmt ]

    def nests_of_declaration(self, declaration: Node) -> List[Node]:
        return [ declaration ]

    def nests_of_function_definition(self, descendent: Node) -> List[Node]:
        # descendent is a descendent of the "function_definition"
        function_definition = descendent.get_descendent_of_types([ CNodeType.FUNCTION_DEFINITION.value ])
        return [ function_definition ]

    def nests_of_translation_unit(self, translation_unit: Node) -> List[Node]:
        return [ translation_unit ]

    def nests_of_goto_statement(self, goto_statement: Node) -> List[Node]:
        return [ goto_statement ]

    def nests(self, cfa: CFA[CFANode]) -> List[Node]:
        nests: List[Node] = list()

        ascendent = cfa.root.node.get_immediate_descendent_of_types(
            [ CNodeType.FUNCTION_DEFINITION.value, CNodeType.TRANSLATION_UNIT.value ]
        )
        if ascendent.is_type(CNodeType.TRANSLATION_UNIT):
            nests.extend(self.nests_of_translation_unit(ascendent))

        for cfa_node in cfa.nodes:
            node: Node = cfa_node.node
            # Case 1: if-statements (Including "else if" and "else")
            if self._syntax.is_condition_of_if(node):
                nests.extend(self.nests_of_if_condition(node))
            # Case 2: while-loops
            if self._syntax.is_condition_of_while(node):
                nests.extend(self.nests_of_while_condition(node))
            # Case 3: do-while-loops
            if self._syntax.is_condition_of_do_while(node):
                nests.extend(self.nests_of_do_while_condition(node))
            # Case 4: for-loop
            # Since a for-loop can exist without a "init", "cond", and "update"
            #   The only persistent aspect of it is the body, which is always included.
            if self._syntax.is_body_of_for_loop(node):
                nests.extend(self.nests_of_for_loop_body(node))
            # Case 5: Switch (Cases and default)
            if self._syntax.is_condition_of_switch(node):
                nests.extend(self.nests_of_case_value_for_switch(node))
            # Case 6: Labels
            if self._syntax.is_labeled_statement(node):
                nests.extend(self.nests_of_labeled_statement(node))
            # Case 7: Expression statement
            if self._syntax.is_expression_statement(node):
                nests.extend(self.nests_of_expression_statement(node))
            # Case 8: Declaration
            if self._syntax.is_declaration(node):
                # TODO: Declarations nests should not be added,
                #   if they are the intiialization of a for-loop.
                nests.extend(self.nests_of_declaration(node))
            # Case 9: Return statement
            if self._syntax.is_return_statement(node):
                nests.extend(self.nests_of_return_statement(node))
            # Case 10: Goto
            if self._syntax.is_goto_statement(node):
                nests.extend(self.nests_of_goto_statement(node))

            # Case 1: First function definition (Begin/end unit)
            if self._syntax.is_immediate_of_function_definition(node):
                nests.extend(self.nests_of_function_definition(node))

        # Remove duplicates
        corrected: List[Node] = list()
        for nest in nests:
            if nest not in corrected:
                corrected.append(nest)

        return corrected

    def infection_spore_expression_statement(self, _: Node) -> List[TreeInfection]:
        return [ ]

    def infection_spore_assignment_statement(self, _: Node) -> List[TreeInfection]:
        return [ ]

    def infection_spore_return_statement(self, _: Node) -> List[TreeInfection]:
        return [ ]

    def infection_spore_declaration(self, _: Node) -> List[TreeInfection]:
        return [ ]

    def infection_spore_if_statement(self, if_stmt: Node) -> List[TreeInfection]:
        infections: List[TreeInfection] = [ ]

        consequence: Node = if_stmt.child_by_field(CField.CONSEQUENCE)
        alternative: Node = if_stmt.child_by_field(CField.ALTERNATIVE)

        consequence_postfix: str = ""
        alternative_postfix: str = ""

        if alternative is None:
            consequence_postfix = self._canary_factory.create_location_tweet()
        elif not self._syntax.has_else_if(if_stmt):
            alternative_postfix = self._canary_factory.create_location_tweet()

        # We dont have to check if "consequence" is None, because every
        #   "if_statement" has a consequence of its "condition"
        infections.extend(self._canary_factory.create_location_tweets(
            consequence,
            pre_infix=self._canary_factory.create_location_tweet(),
            postfix=consequence_postfix
        ))

        # If it is an "else if", then it is handled as a seperate "if"
        if alternative is not None and not self._syntax.has_else_if(if_stmt):
            infections.extend(self._canary_factory.create_location_tweets(
                alternative,
                pre_infix=self._canary_factory.create_location_tweet(),
                postfix=alternative_postfix
            ))

        return infections

    def infection_spore_while_statement(self, while_stmt: Node) -> List[TreeInfection]:
        body: Node = while_stmt.child_by_field(CField.BODY)
        infections: List[TreeInfection] = self._canary_factory.create_location_tweets(
            body,
            pre_infix=self._canary_factory.create_location_tweet(),
            postfix=self._canary_factory.create_location_tweet()
        )
        return infections

    def infection_spore_do_statement(self, do_stmt: Node) -> List[TreeInfection]:
        body: Node = do_stmt.child_by_field(CField.BODY)
        infections: List[TreeInfection] = self._canary_factory.create_location_tweets(
            body,
            pre_infix=self._canary_factory.create_location_tweet(),
        )
        infections.append(
            self._canary_factory.append_location_tweet(do_stmt)
        )
        return infections

    def infection_spore_for_statement(self, for_stmt: Node) -> List[TreeInfection]:
        body: Node = self._syntax.get_for_loop_body(for_stmt)
        # If it is a expression statement then the body is just a ";"
        #   I.e. for(int i = 0; i < 10; ++i);
        #   I.e. for(int i = 0; i < 10; ++i) {TWEET();;TWEET()}
        return self._canary_factory.create_location_tweets(
            body,
            pre_infix=self._canary_factory.create_location_tweet(),
            postfix=self._canary_factory.create_location_tweet(),
        )

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
        infections.append(
            self._canary_factory.append_location_tweet(switch_stmt)
        )
        return infections

    def infection_spore_labeled_statement(self, node: Node) -> List[TreeInfection]:
        # For a "labeled_statement" the second child (index 1) is the ":"
        return [ self._canary_factory.append_location_tweet(node.children[1]) ]

    def infection_spore_function_definition(self, node: Node) -> List[TreeInfection]:
        body = node.child_by_field(CField.BODY)
        left_paren = body.children[0]
        return [ 
            self._canary_factory.append_location_tweet(left_paren),
        ]

    def infection_spore_goto_statement(self, node: Node) -> List[TreeInfection]:
        return [ self._canary_factory.insert_location_tweet(node) ]

    def infection_spore_translation_unit(self, node: Node) -> List[TreeInfection]:
        return [ self._canary_factory.insert_location_tweet(node) ]

    def infect(self, tree: Tree, cfa: CFA[CFANode]) -> Tree:
        probes: Dict[str, Callable[[Node], List[TreeInfection]]] = {
            # Sequential statements
            CNodeType.EXPRESSION_STATEMENT.value: self.infection_spore_expression_statement,
            CNodeType.ASSIGNMENT_EXPRESSION.value: self.infection_spore_expression_statement,
            CNodeType.RETURN_STATEMENT.value: self.infection_spore_return_statement,
            CNodeType.DECLARATION.value: self.infection_spore_declaration,
            # Control structures
            CNodeType.IF_STATEMENT.value: self.infection_spore_if_statement,
            CNodeType.WHILE_STATEMENT.value: self.infection_spore_while_statement,
            CNodeType.DO_STATEMENT.value: self.infection_spore_do_statement,
            CNodeType.FOR_STATEMENT.value: self.infection_spore_for_statement,
            CNodeType.SWITCH_STATEMENT.value: self.infection_spore_switch_statement,
            # Unconditional jump
            CNodeType.LABELED_STATEMENT.value: self.infection_spore_labeled_statement,
            CNodeType.GOTO_STATEMENT.value: self.infection_spore_goto_statement,
            # Additional
            CNodeType.FUNCTION_DEFINITION.value: self.infection_spore_function_definition,
            CNodeType.TRANSLATION_UNIT.value: self.infection_spore_translation_unit
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