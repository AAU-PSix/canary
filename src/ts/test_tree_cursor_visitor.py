import unittest
from typing import Iterable, List

from src.cfa import CFA
from src.cfa.cfa import CFANode

from src.ts import (
    Node,
    LanguageLibrary,
    Parser,
    Query,
    Tree,
    TreeCursor,
    TreeCFAVisitor,
)

class TreeCursorTest(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.query_compound_assignment)
        self._assignment_query: Query = self._language.query(self._language.syntax.query_assignment)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.query_binary_expression)
        return super().setUp()

    def test_pre_order_three_expressions(self) -> None:
        tree: Tree = self._parser.parse("a=1; a=2; a=3;")
        cursor: TreeCursor = tree.walk()
        iterable: Iterable[Node] = cursor.pre_order_traverse(True)
        order: List[Node] = list()

        for node in iterable: order.append(node)

        self.assertEqual(len(order), 13)

        self.assertEqual(order[0].type, "translation_unit")

        self.assertEqual(order[1].type, "expression_statement")
        self.assertEqual(order[2].type, "assignment_expression")
        self.assertEqual(order[3].type, "identifier")
        self.assertEqual(order[4].type, "number_literal")

        self.assertEqual(order[5].type, "expression_statement")
        self.assertEqual(order[6].type, "assignment_expression")
        self.assertEqual(order[7].type, "identifier")
        self.assertEqual(order[8].type, "number_literal")

        self.assertEqual(order[9].type, "expression_statement")
        self.assertEqual(order[10].type, "assignment_expression")
        self.assertEqual(order[11].type, "identifier")
        self.assertEqual(order[12].type, "number_literal")

    def test_tree_visitor_for_cfa_three_expressions(self) -> None:
        tree: Tree = self._parser.parse("a=1; a=2; a=3;")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        visitor.create(tree.root_node)
        order: List[Node] = visitor._order

        self.assertEqual(len(order), 4)
        self.assertEqual(order[0].type, "translation_unit")
        self.assertEqual(order[1].type, "expression_statement")
        self.assertEqual(order[2].type, "expression_statement")
        self.assertEqual(order[3].type, "expression_statement")

    def test_tree_cfa_creation_three_expressions(self) -> None:
        tree: Tree = self._parser.parse("a=1; a=2; a=3;")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        cfa: CFA = visitor.create(tree.root_node)

        self.assertEqual(cfa.node_len, 4)

        curr: CFANode = cfa.root
        self.assertEqual(curr.node.type, "translation_unit")

        outgoing: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0].node.type, "expression_statement")
        curr = outgoing[0]

        outgoing = cfa.outgoing(curr)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0].node.type, "expression_statement")
        curr = outgoing[0]

        outgoing = cfa.outgoing(curr)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0].node.type, "expression_statement")
        curr = outgoing[0]

    def test_pre_order_one_if_statement(self) -> None:
        tree: Tree = self._parser.parse("if (a == 1) { a = 2; }")
        cursor: TreeCursor = tree.walk()
        iterable: Iterable[Node] = cursor.pre_order_traverse(True)
        order: List[Node] = list()

        for node in iterable: order.append(node)

        self.assertEqual(len(order), 11)

        self.assertEqual(order[0].type, "translation_unit")

        self.assertEqual(order[1].type, "if_statement")
        self.assertEqual(order[2].type, "parenthesized_expression")
        self.assertEqual(order[3].type, "binary_expression")
        self.assertEqual(order[4].type, "identifier")
        self.assertEqual(order[5].type, "number_literal")

        self.assertEqual(order[6].type, "compound_statement")
        self.assertEqual(order[7].type, "expression_statement")
        self.assertEqual(order[8].type, "assignment_expression")
        self.assertEqual(order[9].type, "identifier")
        self.assertEqual(order[10].type, "number_literal")

    def test_tree_cfa_creation_one_if_statement(self) -> None:
        tree: Tree = self._parser.parse("if (a == 1) { a = 1; } a = 2;")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        cfa: CFA = visitor.create(tree.root_node)

        self.assertEqual(cfa.node_len, 4)
        self.assertEqual(len(visitor._order), 4)
        self.assertEqual(visitor._order[0].type, "translation_unit")
        self.assertEqual(visitor._order[1].type, "if_statement")
        self.assertEqual(visitor._order[2].type, "expression_statement")
        self.assertEqual(visitor._order[3].type, "expression_statement")

        if_node: CFANode = cfa.outgoing(cfa.root)[0]
        self.assertEqual(if_node.node.type, "parenthesized_expression")

        branches: List[CFANode] = cfa.outgoing(if_node)
        self.assertEqual(len(branches), 2)
        # True branch
        next_true: CFANode = branches[0]
        self.assertEqual(next_true.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_true.node), "a = 1;")
        # False branch
        next_false: CFANode = branches[1]
        self.assertEqual(next_false.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_false.node), "a = 2;")

        # The merge
        next_true = cfa.outgoing(next_true)[0]
        self.assertEqual(next_false.node, next_true.node)
        self.assertEqual(next_true.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_true.node), "a = 2;")

    def test_tree_visitor_for_cfa_one_if_statement(self) -> None:
        tree: Tree = self._parser.parse("if (a == 1) { a = 2; }")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        visitor.create(tree.root_node)
        order: List[Node] = visitor._order

        self.assertEqual(len(order), 3)
        self.assertEqual(order[0].type, "translation_unit")
        self.assertEqual(order[1].type, "if_statement")
        self.assertEqual(order[2].type, "expression_statement")

        self.assertEqual(len(order[1].children), 3)
        self.assertEqual(order[1].children[0].type, "if")
        self.assertEqual(order[1].children[1].type, "parenthesized_expression")
        self.assertEqual(order[1].children[2].type, "compound_statement")

        self.assertEqual(order[1].child_by_field_name("condition").type, "parenthesized_expression")
        self.assertEqual(order[1].child_by_field_name("consequence").type, "compound_statement")
        self.assertIsNone(order[1].child_by_field_name("alternative"))

    def test_tree_visitor_for_cfa_one_if_else_statement(self) -> None:
        tree: Tree = self._parser.parse("if (a == 1) { a = 2; } else { a = 3; }")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        visitor.create(tree.root_node)
        order: List[Node] = visitor._order

        self.assertEqual(len(order), 4)
        self.assertEqual(order[0].type, "translation_unit")
        self.assertEqual(order[1].type, "if_statement")
        self.assertEqual(order[2].type, "expression_statement")
        self.assertEqual(order[2].type, "expression_statement")

        self.assertEqual(len(order[1].children), 5)
        self.assertEqual(order[1].children[0].type, "if")
        self.assertEqual(order[1].children[1].type, "parenthesized_expression")
        self.assertEqual(order[1].children[2].type, "compound_statement")
        self.assertEqual(order[1].children[3].type, "else")
        self.assertEqual(order[1].children[4].type, "compound_statement")

        self.assertEqual(order[1].child_by_field_name("condition").type, "parenthesized_expression")
        self.assertEqual(order[1].child_by_field_name("consequence").type, "compound_statement")
        self.assertEqual(order[1].child_by_field_name("alternative").type, "compound_statement")

    def test_tree_cfa_creation_one_if_else_statement(self) -> None:
        tree: Tree = self._parser.parse("if (a == 1) { a = 2; } else { a = 3; } a = 4;")
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        cfa: CFA = visitor.create(tree.root_node)

        self.assertEqual(cfa.node_len, 5)
        self.assertEqual(len(visitor._order), 5)
        self.assertEqual(visitor._order[0].type, "translation_unit")
        self.assertEqual(visitor._order[1].type, "if_statement")
        self.assertEqual(visitor._order[2].type, "expression_statement")
        self.assertEqual(visitor._order[3].type, "expression_statement")
        self.assertEqual(visitor._order[4].type, "expression_statement")

        if_node: CFANode = cfa.outgoing(cfa.root)[0]
        self.assertEqual(if_node.node.type, "parenthesized_expression")

        branches: List[CFANode] = cfa.outgoing(if_node)
        self.assertEqual(len(branches), 2)
        # True branch
        next_true: CFANode = branches[0]
        self.assertEqual(next_true.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_true.node), "a = 2;")
        # False branch
        next_false: CFANode = branches[1]
        self.assertEqual(next_false.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_false.node), "a = 3;")

        # The merge
        next_true = cfa.outgoing(next_true)[0]
        next_false = cfa.outgoing(next_false)[0]
        self.assertEqual(next_true.node, next_false.node)
        self.assertEqual(next_true.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(next_true.node), "a = 4;")

    def test_tree_visitor_for_cfa_one_if_elseif_else_statement(self) -> None:
        tree: Tree = self._parser.parse(
            "if (a == 1) { a = 2; } else if (a == 2) { } else { a = 3; }"
        )
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        visitor.create(tree.root_node)
        order: List[Node] = visitor._order

        self.assertEqual(len(order), 5)
        self.assertEqual(order[0].type, "translation_unit")
        self.assertEqual(order[1].type, "if_statement")
        self.assertEqual(order[2].type, "expression_statement")
        self.assertEqual(order[3].type, "if_statement")
        self.assertEqual(order[4].type, "expression_statement")

        self.assertEqual(len(order[1].children), 5)
        self.assertEqual(order[1].children[0].type, "if")
        self.assertEqual(order[1].children[1].type, "parenthesized_expression")
        self.assertEqual(order[1].children[2].type, "compound_statement")
        self.assertEqual(order[1].children[3].type, "else")
        self.assertEqual(order[1].children[4].type, "if_statement")

        self.assertEqual(order[1].child_by_field_name("condition").type, "parenthesized_expression")
        self.assertEqual(tree.contents_of(
            order[1].child_by_field_name("condition")),
            "(a == 1)"
        )
        self.assertEqual(order[1].child_by_field_name("consequence").type, "compound_statement")
        self.assertEqual(tree.contents_of(
            order[1].child_by_field_name("consequence")),
            "{ a = 2; }"
        )
        self.assertEqual(order[1].child_by_field_name("alternative").type, "if_statement")
        self.assertEqual(
            tree.contents_of(order[1].child_by_field_name("alternative")),
            "if (a == 2) { } else { a = 3; }"
        )

        self.assertEqual(len(order[1].children), 5)
        self.assertEqual(order[3].children[0].type, "if")
        self.assertEqual(order[3].children[1].type, "parenthesized_expression")
        self.assertEqual(order[3].children[2].type, "compound_statement")
        self.assertEqual(order[3].children[3].type, "else")
        self.assertEqual(order[3].children[4].type, "compound_statement")

        self.assertEqual(order[3].child_by_field_name("condition").type, "parenthesized_expression")
        self.assertEqual(tree.contents_of(
            order[3].child_by_field_name("condition")),
            "(a == 2)"
        )
        self.assertEqual(order[3].child_by_field_name("consequence").type, "compound_statement")
        self.assertEqual(tree.contents_of(
            order[3].child_by_field_name("consequence")),
            "{ }"
        )
        self.assertEqual(order[3].child_by_field_name("alternative").type, "compound_statement")
        self.assertEqual(
            tree.contents_of(order[3].child_by_field_name("alternative")),
            "{ a = 3; }"
        )

    def test_tree_visitor_for_cfa_switch_one_case(self) -> None:
        tree: Tree = self._parser.parse(
            """
            switch (expression) {
                case a: a = 2;
            }
            """
        )
        visitor: TreeCFAVisitor = TreeCFAVisitor()
        visitor.create(tree.root_node)
        order: List[Node] = visitor._order