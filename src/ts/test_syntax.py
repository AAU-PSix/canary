from unittest import TestCase

from . import (
    Node,
    Tree,
    Parser,
    LanguageLibrary
)
from .c_syntax import CField, CNodeType, CSyntax

class TestCSyntax2(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._parser = Parser.c()
        self._syntax = CSyntax()
        return super().setUp()

    def test_is_field_true(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root_node \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.is_field(
            node_plain_assignment.type,
            CNodeType.PLAIN_ASSIGNMENT
        )

        self.assertTrue(actual)

    def test_is_field_false(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root_node \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.is_field(
            node_plain_assignment.type,
            CNodeType.LOGICAL_AND
        )

        self.assertFalse(actual)

    def test_in_fields_true(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root_node \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.in_fields(
            node_plain_assignment.type,
            [ CNodeType.PLAIN_ASSIGNMENT, CNodeType.LOGICAL_AND]
        )

        self.assertTrue(actual)

    def test_in_fields_false(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root_node \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.in_fields(
            node_plain_assignment.type,
            [ CNodeType.LOGICAL_AND, CNodeType.LOGICAL_OR ]
        )

        self.assertFalse(actual)

    def test_node_field_plain_assignment(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root_node \
            .named_children[0] \
            .named_children[0] \
            .children[1]
        expected = CNodeType.PLAIN_ASSIGNMENT

        actual = self._syntax.node_field(
            node_plain_assignment.type
        )

        self.assertEqual(actual, expected)

    def test_child_plain_assignment(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_assignment_expression: Node = tree.root_node \
            .named_children[0] \
            .named_children[0]
        expected = CNodeType.IDENTIFIER.value

        actual = self._syntax.child_by_field(
            node_assignment_expression,
            CField.LEFT
        ).type

        self.assertEqual(actual, expected)