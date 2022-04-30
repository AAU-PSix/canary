from typing import List, Tuple
from sys import float_info
import unittest

from mutator.ocor_strategy import OcorStrategy
from ts.c_syntax import CSyntax
from . import (
    Mutator,
    Parser,
)
from ts import (
    LanguageLibrary,
    Capture,
    Node,
    NodeType,
    Query,
)

class TestMutatorOcor(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._mutator: Mutator = Mutator(self._parser)
        self._syntax = CSyntax()

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.compound_assignment_query)
        self._assignment_query: Query = self._language.query(self._language.syntax.assignment_query)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.binary_expression_query)
        return super().setUp()


    def parse_first_binary_expression_operator(self, binary_query: Query, expression: str) -> Node:
            root: Node = self._parser.parse(expression).root
            self.assertEqual(root.type, "translation_unit")
            captures: Capture = binary_query.captures(root)
            self.assertEqual(len(captures), 1)
            operator_node: Node = captures.first()[0]
            operator: Node = self._language.syntax.get_binary_expression_operator(operator_node)
            return operator

    def create_range_checks(self, ranges: List[List[str]]) -> "List[tuple(str, float, float)]":
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

    def assert_domain_and_ranges(self, binary_query: Query, domain: List[NodeType], range_checks: List[Tuple[NodeType, float, float]]):
        for domain_operator in domain:
            operator: Node = self.parse_first_binary_expression_operator(binary_query, f'a{domain_operator.value}b')

            for range_section in range_checks:
                actual: NodeType = OcorStrategy(self._parser).ocor(operator, range_section[1], range_section[2])
                self.assertEqual(operator.type, domain_operator.value)
                self.assertEqual(actual.value, range_section[0].value)


    def test_ocor_capture_operators(self) -> None:

        program = """
             b += 2;
             c &= 1;
             a && b;
             a < b;
             a << b;
             time = 5;
             time = a = b;
             """
        tree = self._parser.parse(program)

        ocor = OcorStrategy(self._parser)
        capture = ocor.capture(tree.root)
        
        self.assertTrue(len(capture) == 5)        
        self.assertTrue( "+=" == capture[0].type)
        self.assertTrue( "&=" == capture[1].type)
        self.assertTrue( "&&" == capture[2].type)
        self.assertTrue( "<" == capture[3].type)
        self.assertTrue( "<<" == capture[4].type)

        for element in capture:
            self.assertTrue("=" != element.type)

    def test_ocor_capture_in_function(self) -> None:

        program = """
             void foo() {
                 int a = 0;
                 int b;
                 double c;
                 for (b = 0; b < 10; ++b) {
                     print(b);
                     if (b % 2 == 0) {
                         continue;
                     }
                    b /= 2;
                 }
                 b /= 2; a += 2; c = 42;
                 a = b = c;
                 return;
             }
             """
        tree = self._parser.parse(program)

        ocor = OcorStrategy(self._parser)
        capture = ocor.capture(tree.root)
     
        self.assertTrue(len(capture) == 6 )
        self.assertTrue( "<" == capture[0].type)
        self.assertTrue( "==" == capture[1].type)
        self.assertTrue( "%" == capture[2].type)
        self.assertTrue( "/=" == capture[3].type)
        self.assertTrue( "/=" == capture[4].type)
        self.assertTrue( "+=" == capture[5].type)
        
        for element in capture:
            self.assertTrue("=" != element.type)


    def test_ocor_ranges_oaaa(self) -> None:
        domain: List[str] = self._language.syntax.arithmetic_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OAAA
                self._language.syntax.arithmetic_compound_assignment
            ]
        )
        self.assert_domain_and_ranges(self._compound_assignment_query, domain, range_checks)

    def test_ocor_ranges_oaan(self) -> None:
        domain: List[str] = self._language.syntax.arithmetic_operators
        range_checks = self.create_range_checks(
            [
                # OAAN
                self._language.syntax.arithmetic_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_obba(self) -> None:
        domain: List[str] = self._language.syntax.bitwise_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OBBA
                self._language.syntax.bitwise_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_obbn(self) -> None:
        domain: List[str] = self._language.syntax.bitwise_operators
        range_checks = self.create_range_checks(
            [
                # OBBN
                self._language.syntax.bitwise_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_olln(self) -> None:
        domain: List[str] = self._language.syntax.logical_operators
        range_checks = self.create_range_checks(
            [
                # OLLN
                self._language.syntax.logical_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_orrn(self) -> None:
        domain: List[str] = self._language.syntax.relational_operators
        range_checks = self.create_range_checks(
            [
                # ORRN
                self._language.syntax.relational_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_ossa(self) -> None:
        domain: List[str] = self._language.syntax.shift_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OSSA
                self._language.syntax.shift_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_ocor_ranges_ossn(self) -> None:
        domain: List[str] = self._language.syntax.shift_operators
        range_checks = self.create_range_checks(
            [
                # OSSN
                self._language.syntax.shift_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)