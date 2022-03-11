from sys import float_info
from typing import Dict
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

    def parse_first_augmented_assignment_expression_operator(self, expression: str) -> Node:
            root: Node = self._parser.parse(expression).root_node
            captures: List[Tuple[Node, str]] = self._compound_assignment_query.captures(root)
            operator: Node = captures[0][0].children[1]
            return operator

    def parse_first_binary_expression_operator(self, expression: str) -> Node:
            root: Node = self._parser.parse(expression).root_node
            captures: List[Tuple[Node, str]] = self._binary_expression_query.captures(root)
            operator: Node = captures[0][0].children[1]
            return operator

    def test_obom_ranges_oaba_oaea_oasa(self) -> None:
        domain: List[str] = self._language.arithmetic_compound_assignment
        range: List[tuple(str, float, float)] = [
            # OABA
            ("|=", 0, 0),
            ("|=", 0, 1/3 - float_info.epsilon),
            ("&=", 0, 1/3),
            ("&=", 0, 2/3 - float_info.epsilon),
            ("^=", 0, 2/3),
            ("^=", 0, 1 - float_info.epsilon),
            # OAEA
            ("=", 1/3, 0),
            ("=", 1/3, 1 - float_info.epsilon),
            # OASA
            ("<<=", 2/3, 0),
            (">>=", 2/3, 1 - float_info.epsilon),
        ]
        for domain_operator in domain:
            operator: Node = self.parse_first_augmented_assignment_expression_operator(f'a{domain_operator}b')

            for range_section in range:
                actual: str = self._mutator.obom(operator, range_section[1], range_section[2])
                self.assertEqual(operator.type, domain_operator)
                self.assertEqual(actual, range_section[0])