from importlib.resources import path
import unittest
import graphviz

from src.ts import *
from src.cfa import *
from . import TreeInfestator

class TestTreeInfestator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._infestator = TreeInfestator(self._parser)

    def test_is_condition_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        condition: Node = if_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._infestator.is_condition_of_if(condition)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        alternative: Node = if_node.child_by_field_name("alternative")
        expected: bool = False

        actual = self._infestator.is_condition_of_if(alternative)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(alternative.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_nests_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        first_if_statement: Node = tree.root_node.named_children[0]
        first_if_consequence: Node = first_if_statement.child_by_field_name("consequence")
        second_if_statement: Node = first_if_consequence.named_children[0]
        second_if_consequence: Node = second_if_statement.child_by_field_name("consequence")

        nests = self._infestator.nests(cfa)

        self.assertEqual(2, len(nests))
        self.assertEqual(first_if_consequence.type, "compound_statement")
        self.assertEqual(second_if_consequence.type, "compound_statement")

        self.assertEqual(nests[0].type, "compound_statement")
        self.assertEqual(nests[0].start_byte, second_if_consequence.start_byte)

        self.assertEqual(nests[1].type, "compound_statement")
        self.assertEqual(nests[1].start_byte, first_if_consequence.start_byte)

    def test_infect_if(self) -> None:
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_else(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif(self) -> None:
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else if(a) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif_else(self) -> None:
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); if(a) {TWEET(); } }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect(self) -> None:
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)
        actual: Tree = self._infestator.infect(tree, cfa)
        self.assertEqual(actual.text, "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }")

    def test_can_add_tweet_for_if_statement(self):
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_else_statement(self):
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_statement(self):
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else if(a) {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_else_statement(self):
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_statement(self):
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_else_statement(self):
        program: str = "if(a) { if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else if(a) {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_else_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa)
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); } }"
        self.assertEqual(expected, actual.text)