from typing import Iterable
import unittest
from ts import Node, Language
from . import (
    LanguageLibrary,
    Parser,
    Query,
    Tree,
    TreeCursor,
)

class TreeCursorTest(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.compound_assignment_query)
        self._assignment_query: Query = self._language.query(self._language.syntax.assignment_query)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.binary_expression_query)
        return super().setUp()

    def test_pre_order_traverse(self) -> None:
        tree: Tree = self._parser.parse("if (n < 0) { return 0; }")
        cursor: TreeCursor = tree.walk()
        traverser: Iterable[Node] = cursor.pre_order_traverse(
            named_only=True,
        )

        node: Node = next(traverser)
        self.assertEqual(node.type, "translation_unit")
        node: Node = next(traverser)
        self.assertEqual(node.type, "if_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "parenthesized_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "binary_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "identifier")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")
        node: Node = next(traverser)
        self.assertEqual(node.type, "compound_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "return_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")

    def test_pre_order_traverse_break(self) -> None:
        tree: Tree = self._parser.parse("if (n < 0) { return 0; }")
        cursor: TreeCursor = tree.walk()
        traverser: Iterable[Node] = cursor.pre_order_traverse(
            named_only=True,
        )
        
        for _ in traverser:
            break

        node: Node = next(traverser)
        self.assertEqual(node.type, "if_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "parenthesized_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "binary_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "identifier")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")
        node: Node = next(traverser)
        self.assertEqual(node.type, "compound_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "return_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")

    def test_breadth_first_traversal(self) -> None:
        tree: Tree = self._parser.parse("if (n < 0) { return 0; }")
        cursor: TreeCursor = tree.walk()
        traverser: Iterable[Node] = cursor.breadth_first_traverse(
            named_only=True,
        )

        node: Node = next(traverser)
        self.assertEqual(node.type, "translation_unit")
        node: Node = next(traverser)
        self.assertEqual(node.type, "if_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "parenthesized_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "compound_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "binary_expression")
        node: Node = next(traverser)
        self.assertEqual(node.type, "return_statement")
        node: Node = next(traverser)
        self.assertEqual(node.type, "identifier")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")
        node: Node = next(traverser)
        self.assertEqual(node.type, "number_literal")