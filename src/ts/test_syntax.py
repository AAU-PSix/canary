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
        node_plain_assignment: Node = tree.root \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.is_type(
            node_plain_assignment.type,
            CNodeType.PLAIN_ASSIGNMENT
        )

        self.assertTrue(actual)

    def test_is_field_false(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.is_type(
            node_plain_assignment.type,
            CNodeType.LOGICAL_AND
        )

        self.assertFalse(actual)

    def test_in_fields_true(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.in_types(
            node_plain_assignment.type,
            [ CNodeType.PLAIN_ASSIGNMENT, CNodeType.LOGICAL_AND]
        )

        self.assertTrue(actual)

    def test_in_fields_false(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root \
            .named_children[0] \
            .named_children[0] \
            .children[1]

        actual = self._syntax.in_types(
            node_plain_assignment.type,
            [ CNodeType.LOGICAL_AND, CNodeType.LOGICAL_OR ]
        )

        self.assertFalse(actual)

    def test_node_field_plain_assignment(self) -> None:
        tree: Tree = self._parser.parse("a=1;")
        node_plain_assignment: Node = tree.root \
            .named_children[0] \
            .named_children[0] \
            .children[1]
        expected = CNodeType.PLAIN_ASSIGNMENT

        actual = self._syntax.node_field(
            node_plain_assignment.type
        )

        self.assertEqual(actual, expected)

    def test_get_immediate_descendent_of_types_field(self) -> None:
        tree: Tree = self._parser.parse("void Foo() { return; }")
        return_stmt: Node = tree.root.named_children[0] \
            .child_by_field(CField.BODY) \
            .named_children[0]

        function_definition = return_stmt.get_immediate_descendent_of_types_field(
            [ CNodeType.FUNCTION_DEFINITION.value ], CField.BODY
        )

        self.assertTrue(function_definition.is_type(CNodeType.FUNCTION_DEFINITION))

    def test_get_immediate_descendent_of_types_field_none(self) -> None:
        tree: Tree = self._parser.parse("void Foo() { a=b; return; }")
        return_stmt: Node = tree.root.named_children[0] \
            .child_by_field(CField.BODY) \
            .named_children[1]

        function_definition = return_stmt.get_immediate_descendent_of_types_field(
            [ CNodeType.FUNCTION_DEFINITION.value ], CField.BODY
        )

        self.assertIsNone(function_definition)

    def test_is_immediate_of_function_definition_true(self) -> None:
        tree: Tree = self._parser.parse(
        """
        int add(int a, int b) {
            int sum = a + b;
            return sum;
        }
        """)
        first_stmt: Node = tree.root.named_children[0] \
            .child_by_field(CField.BODY) \
            .named_children[0]
        syntax = CSyntax()

        is_immediate = syntax.is_immediate_of_function_definition(first_stmt)

        self.assertTrue(is_immediate)

    def test_is_immediate_of_function_definition_false(self) -> None:
        tree: Tree = self._parser.parse(
        """
        int add(int a, int b) {
            int sum = a + b;
            return sum;
        }
        """
        )
        second_stmt: Node = tree.root.named_children[0] \
            .child_by_field(CField.BODY) \
            .named_children[1]
        syntax = CSyntax()

        is_immediate = syntax.is_immediate_of_function_definition(second_stmt)

        self.assertFalse(is_immediate)

    def test_is_body_of_for_loop_1(self) -> None:
        syntax = CSyntax()
        tree: Tree = self._parser.parse(
            """
            for (;;) { if(a) { a=2; } }
            """
        )
        for_statement = tree.root.first_named_child
        compound_statement = for_statement.first_named_child
        if_statement = compound_statement.first_named_child
        condition = if_statement.child_by_field(CField.CONDITION)
        consequence = if_statement.child_by_field(CField.CONSEQUENCE)

        self.assertTrue(for_statement.is_type(CNodeType.FOR_STATEMENT))
        actual = syntax.is_body_of_for_loop(for_statement)
        self.assertFalse(actual)

        self.assertTrue(compound_statement.is_type(CNodeType.COMPOUND_STATEMENT))
        actual = syntax.is_body_of_for_loop(compound_statement)
        self.assertTrue(actual)

        self.assertTrue(if_statement.is_type(CNodeType.IF_STATEMENT))
        actual = syntax.is_body_of_for_loop(if_statement)
        self.assertTrue(actual)

        self.assertTrue(condition.is_type(CNodeType.PARENTHESIZED_EXPRESSION))
        actual = syntax.is_body_of_for_loop(condition)
        self.assertTrue(actual)

        self.assertTrue(consequence.is_type(CNodeType.COMPOUND_STATEMENT))
        actual = syntax.is_body_of_for_loop(consequence)
        self.assertFalse(actual)