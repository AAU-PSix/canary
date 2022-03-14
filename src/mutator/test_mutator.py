import unittest
from . import *

class TestMutator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._mutator: Mutator = Mutator(self._parser)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.query_compound_assignment)
        self._assignment_query: Query = self._language.query(self._language.syntax.query_assignment)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.query_binary_expression)
        return super().setUp()
