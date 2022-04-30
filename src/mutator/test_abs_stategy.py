from unittest import TestCase
from .abs_stategy import AbsStrategy
from ts import (
    LanguageLibrary,
    Parser,
    CSyntax,
)

class TestAbsStrategu(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._syntax = CSyntax()

    def test_capture_binary_expression(self) -> None:
        program = "A = b + c"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_binary_expression(self) -> None:
        program = "A = b + c"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_binary_expression(self) -> None:
        program = "A = b + c"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "A = -(b + c)")

    def test_capture_unary_expression(self) -> None:
        program = "A = -b"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_unary_expression(self) -> None:
        program = "A = -b"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_unary_expression(self) -> None:
        program = "A = -b"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "A = -(-b)")

    def test_capture_number_literal(self) -> None:
        program = "A = 1"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_number_literal(self) -> None:
        program = "A = 1"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_number_literal(self) -> None:
        program = "A = 1"
        tree = self._parser.parse(program)
        stategy = AbsStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "A = -(1)")