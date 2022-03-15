
import unittest
from typing import Iterable, List
from src.cfa.cfa import CFA, CFANode

from . import (
    Node,
    LanguageLibrary,
    Parser,
    Query,
    Tree,
    TreeCursor,
    TreeCursorVisitor,
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

        self.assertEqual(order[0].type, "translation_unit")

        self.assertEqual(order[1].type, "expression_statement")
        self.assertEqual(order[2].type, "assignment_expression")
        self.assertEqual(order[3].type, "identifier")
        self.assertEqual(order[4].type, "number_literal")

    def test_visit_empty(self) -> None:
        tree: Tree = self._parser.parse("")
        visitor: TreeCursorVisitor = TreeCursorVisitor()
        cfa: CFA = visitor.accept(tree.root_node)

        curr: CFANode = cfa.root
        self.assertEqual(curr.node.type, "translation_unit")

    def test_visit_one_expression_statement(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        visitor: TreeCursorVisitor = TreeCursorVisitor()
        cfa: CFA = visitor.accept(tree.root_node)

        curr: CFANode = cfa.root
        self.assertEqual(curr.node.type, "translation_unit")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=1;")

    def test_visit_two_expression_statement(self) -> None:
        tree: Tree = self._parser.parse("a=1; a=2;")
        visitor: TreeCursorVisitor = TreeCursorVisitor()
        cfa: CFA = visitor.accept(tree.root_node)

        curr: CFANode = cfa.root
        self.assertEqual(curr.node.type, "translation_unit")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=1;")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=2;")

    def test_visit_three_expression_statement(self) -> None:
        tree: Tree = self._parser.parse("a=1; a=2; a=3;")
        visitor: TreeCursorVisitor = TreeCursorVisitor()
        cfa: CFA = visitor.accept(tree.root_node)

        curr: CFANode = cfa.root
        self.assertEqual(curr.node.type, "translation_unit")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=1;")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=2;")

        children: List[CFANode] = cfa.outgoing(curr)
        self.assertEqual(len(children), 1)
        curr = children[0]
        self.assertEqual(curr.node.type, "expression_statement")
        self.assertEqual(tree.contents_of(curr.node), "a=3;")

#    def test_visit_one_if_statement_1(self) -> None:
#        tree: Tree = self._parser.parse("if (a == 1) { a = 2; }")
#        visitor: TreeCursorVisitor = TreeCursorVisitor()
#        cfa: CFA = visitor.accept(tree.root_node)
#
#        curr: CFANode = cfa.root
#        self.assertEqual(curr.node.type, "translation_unit")
#
#        children: List[CFANode] = cfa.outgoing(curr)
#        self.assertEqual(len(children), 1)
#        curr = children[0]
#        self.assertEqual(curr.node.type, "parenthesized_expression")
#        self.assertEqual(tree.contents_of(curr.node), "(a == 1)")
#
#        children: List[CFANode] = cfa.outgoing(curr)
#        self.assertEqual(len(children), 1)
#        curr = children[0]
#        self.assertEqual(curr.node.type, "expression_statement")
#        self.assertEqual(tree.contents_of(curr.node), "a = 2;")

#    def test_visit_one_if_statement_2(self) -> None:
#        tree: Tree = self._parser.parse("if (a == 1) { a = 1; } a = 2;")
#        cursor: TreeCursor = tree.walk()
#        visitor: TreeCursorVisitor = TreeCursorVisitor()
#        cfa: CFA = visitor.accept(cursor)
#
#        curr: CFANode = cfa.root
#        self.assertEqual(curr.node.type, "translation_unit")
#
#        children: List[CFANode] = cfa.outgoing(curr)
#        self.assertEqual(len(children), 1)
#        curr = children[0]
#        self.assertEqual(curr.node.type, "parenthesized_expression")
#        self.assertEqual(tree.contents_of(curr.node), "(a == 1)")
#
#        children: List[CFANode] = cfa.outgoing(curr)
#        self.assertEqual(len(children), 2)
#        curr = children[0]
#        self.assertEqual(curr.node.type, "expression_statement")
#        self.assertEqual(tree.contents_of(curr.node), "a = 1;")
#        curr = children[1]
#        self.assertEqual(curr.node.type, "expression_statement")
#        self.assertEqual(tree.contents_of(curr.node), "a = 2;")