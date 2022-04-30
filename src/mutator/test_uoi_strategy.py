from unittest import TestCase
from .uoi_strategy import UoiStrategy
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
    
    def test_capture_update_expression(self) -> None:
        program = "--a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_update_expression(self) -> None:
        program = "--a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_update_expression(self) -> None:
        program = "--a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "++a;")

    def test_capture_arithmetic_unary_expression(self) -> None:
        program = "-a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_arithmetic_unary_expression(self) -> None:
        program = "-a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_arithmetic_unary_expression(self) -> None:
        program = "-a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "+a;")


    def test_capture_logical_unary_expression(self) -> None:
        program = "!a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_logical_unary_expression(self) -> None:
        program = "!a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 1)

    def test_mutate_logical_unary_expression(self) -> None:
        program = "!a;"
        tree = self._parser.parse(program)
        stategy = UoiStrategy(self._parser)

        mutation = stategy.mutate(
            tree, tree.root
        )

        self.assertEqual(mutation.text, "a;")