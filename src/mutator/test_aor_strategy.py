from unittest import TestCase
from .aor_strategy import AorStrategy
from ts import (
    LanguageLibrary,
    Parser,
    CSyntax,
)

class TestLcrStrategu(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._syntax = CSyntax()

    def test_capture_binary_expression(self) -> None:
        program = "b + c;"
        tree = self._parser.parse(program)
        stategy = AorStrategy(self._parser)

        candidates = stategy.capture(tree.root)

        self.assertEqual(len(candidates), 1)

    def test_mutations_binary_expression(self) -> None:
        program = "b + c;"
        tree = self._parser.parse(program)
        stategy = AorStrategy(self._parser)

        mutations = stategy.mutations(
            self._parser, tree, tree.root
        )

        self.assertEqual(len(mutations), 4)


