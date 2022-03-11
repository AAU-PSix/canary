from cgitb import reset
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

    def parse_first_binary_expression_operator(self, binary_infix_expression: Query, expression: str) -> Node:
            root: Node = self._parser.parse(expression).root_node
            captures: List[Tuple[Node, str]] = binary_infix_expression.captures(root)
            operator: Node = captures[0][0].children[1]
            return operator

    def create_range_checks(self, ranges: List[List[str]]) -> "List[tuple(str, float, float)]":
        """Generates the bounds to check for expected ranges

        Returns:
            List[tuple(str, float, float)]: First element is the expected range operator, 
            the range value, and then lastly the range operator value. 
            Theses values are clamped between [0,1)

        Example for Domain: Arithmetic assignment for OABA, OAEA, OASA:
        return List[tuple(str, float, float)] = [
            # OABA
            ('|=', 0.0, 0.0),
            ('|=', 0.0, 1/3 - epsilon),
            ('|=', 1/3 - epsilon, 0.0),
            ('|=', 1/3 - epsilon, 1/3 - epsilon),
            ('&=', 0.0, 1/3),
            ('&=', 0.0, 2/3 - epsilon),
            ('&=', 1/3 - epsilon, 1/3),
            ('&=', 1/3 - epsilon, 2/3 - epsilon),
            ('^=', 0.0, 2/3),
            ('^=', 0.0, 3/3 - epsilon),
            ('^=', 1/3 - epsilon, 2/3),
            ('^=', 1/3 - epsilon, 3/3 - epsilon),
            # OAEA
            ('=', 1/3, 0.0),
            ('=', 1/3, 3/3 - epsilon),
            ('=', 2/3 - epsilon, 0.0),
            ('=', 2/3 - epsilon, 3/3 - epsilon),
            # OASA
            ('<<=', 2/3, 0.0),
            ('<<=', 2/3, 1/2 - epsilon),
            ('<<=', 3/3 - epsilon, 0.0),
            ('<<=', 3/3 - epsilon, 1/2 - epsilon),
            ('>>=', 2/3, 1/2),
            ('>>=', 2/3, 3/3 - epsilon),
            ('>>=', 3/3 - epsilon, 1/2),
            ('>>=', 3/3 - epsilon, 3/3 - epsilon)
        ]
        """
        result: List[tuple(str, float, float)] = []
        for range_idx, range in enumerate(ranges):
            for operator_idx, range_operator in enumerate(range):
                range_lower: float = range_idx / len(ranges)
                range_upper: float = (range_idx + 1) / len(ranges) - float_info.epsilon
                range_operator_lower: float = operator_idx / len(range)
                range_operator_upper: float = (operator_idx + 1) / len(range) - float_info.epsilon
                result.append((range_operator, range_lower, range_operator_lower))
                result.append((range_operator, range_lower, range_operator_upper))
                result.append((range_operator, range_upper, range_operator_lower))
                result.append((range_operator, range_upper, range_operator_upper))
        return result

    def assert_domain_and_ranges(self, binary_infix_expression: Query, domain: List[str], range_checks: "List[tuple(str, float, float)]"):
        for domain_operator in domain:
            operator: Node = self.parse_first_binary_expression_operator(binary_infix_expression, f'a{domain_operator}b')

            for range_section in range_checks:
                actual: str = self._mutator.obom(operator, range_section[1], range_section[2])
                self.assertEqual(operator.type, domain_operator)
                self.assertEqual(actual, range_section[0])

    def test_obom_ranges_oaba_oaea_oasa(self) -> None:
        domain: List[str] = self._language.arithmetic_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OABA
                self._language._bitwise_compound_assignment,
                # OAEA
                [ self._language.plain_assignment ],
                # OASA
                self._language.shift_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._compound_assignment_query, domain, range_checks)

    def test_obom_oabn_oaln_oarn_oasn(self) -> None:
        domain: List[str] = self._language.arithmetic_operators
        range_checks = self.create_range_checks(
            [
                # OABN
                self._language.bitwise_operators,
                # OALN
                self._language.logical_operators,
                # OARN
                self._language.relational_opearators,
                # OASN
                self._language.shift_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)