from sre_constants import SRE_FLAG_LOCALE
from . import *

import unittest

class TestMutationAnalyser(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.js()
        self._parser = Parser.create_with_language(self._language)
        self._mutator: MutationAnalyser = MutationAnalyser(self._parser, self._language)
        
        self._compound_assignment_query: Query = self._language.query("((augmented_assignment_expression) @exp)")
        self._binary_expression_query: Query = self._language.query("((binary_expression) @exp)")
        return super().setUp()

    def test_obom_aritmetic_assignment_domain_bitwise_assignment_range(self) -> None:
        root: Node = self._parser.parse("a+=b").root_node
        captures: List[Tuple[Node, str]] = self._compound_assignment_query.captures(root)
        operator: Node = captures[0][0].children[1]

        actual: str = self._mutator.obom(operator, 0, 0)

        self.assertEqual(operator.type, '+=')
        self.assertEqual(actual, '|=')