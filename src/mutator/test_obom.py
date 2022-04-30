from typing import List, Tuple
from sys import float_info
import unittest

from .obom_strategy import ObomStrategy
from . import (
    Mutator,
    Parser,
)
from ts import (
    LanguageLibrary,
    Query,
    NodeType,
    Node,
    Capture,
)

class TestMutatorObom(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._mutator: Mutator = Mutator(self._parser)

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
        """Generates the bounds to check for expected ranges

        Returns:
            List[tuple(str, float, float)]: First element is the expected range operator, 
            the range value, and then lastly the range operator value. 
            Theses values are clamped between [0,1)

        Example for Domain: Arithmetic assignment for OABA, OAEA, OASA:
        return List[tuple(str, float, float)] = [
            
            OABA
            
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
            
            OAEA
            
            ('=', 1/3, 0.0),
            
            ('=', 1/3, 3/3 - epsilon),
            
            ('=', 2/3 - epsilon, 0.0),
            
            ('=', 2/3 - epsilon, 3/3 - epsilon),
            
            OASA
            
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

    def assert_domain_and_ranges(self, binary_query: Query, domain: List[NodeType], range_checks: List[Tuple[NodeType, float, float]]):
        for domain_operator in domain:
            operator: Node = self.parse_first_binary_expression_operator(binary_query, f'a{domain_operator.value}b')

            for range_section in range_checks:
                actual: NodeType = ObomStrategy(self._parser).obom(operator, range_section[1], range_section[2])
                self.assertEqual(operator.type, domain_operator.value)
                self.assertEqual(actual.value, range_section[0].value)

    def test_obom_ranges_oaba_oaea_oasa(self) -> None:
        domain: List[str] = self._language.syntax.arithmetic_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OABA
                self._language.syntax.bitwise_compound_assignment,
                # OAEA
                self._language.syntax.plain_assignment,
                # OASA
                self._language.syntax.shift_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._compound_assignment_query, domain, range_checks)

    def test_obom_oabn_oaln_oarn_oasn(self) -> None:
        domain: List[str] = self._language.syntax.arithmetic_operators
        range_checks = self.create_range_checks(
            [
                # OABN
                self._language.syntax.bitwise_operators,
                # OALN
                self._language.syntax.logical_operators,
                # OARN
                self._language.syntax.relational_operators,
                # OASN
                self._language.syntax.shift_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_obom_oban_obln_obrn_obsn(self) -> None:
        domain: List[str] = self._language.syntax.bitwise_operators
        range_checks = self.create_range_checks(
            [
                # OBAN
                self._language.syntax.arithmetic_operators,
                # OBLN
                self._language.syntax.logical_operators,
                # OBRN
                self._language.syntax.relational_operators,
                # OBSN
                self._language.syntax.shift_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_obom_obaa_obea_obsa(self) -> None:
        domain: List[str] = self._language.syntax.bitwise_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OBAA
                self._language.syntax.arithmetic_compound_assignment,
                # OBEA
                self._language.syntax.plain_assignment,
                # OBSA
                self._language.syntax.shift_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._compound_assignment_query, domain, range_checks)

    def test_obom_oeaa_oeba_oesa(self) -> None:
        domain: List[str] = self._language.syntax.plain_assignment
        range_checks = self.create_range_checks(
            [
                # OEAA
                self._language.syntax.arithmetic_compound_assignment,
                # OEBA
                self._language.syntax.bitwise_compound_assignment,
                # OESA
                self._language.syntax.shift_compound_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._assignment_query, domain, range_checks)

    def test_olan_olbn_olrn_olsn_osln(self) -> None:
        domain: List[str] = self._language.syntax.logical_operators
        range_checks = self.create_range_checks(
            [
                # OLAN
                self._language.syntax.arithmetic_operators,
                # OLBN
                self._language.syntax.bitwise_operators,
                # OLRN
                self._language.syntax.relational_operators,
                # OLSN
                self._language.syntax.shift_operators,
                # OSLN
                self._language.syntax.logical_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_obom_oran_orbn_orln_orsn(self) -> None:
        domain: List[str] = self._language.syntax.relational_operators
        range_checks = self.create_range_checks(
            [
                # ORAN
                self._language.syntax.arithmetic_operators,
                # ORBN
                self._language.syntax.bitwise_operators,
                # ORLN
                self._language.syntax.logical_operators,
                # ORSN
                self._language.syntax.shift_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_obom_osaa_osba_osea(self) -> None:
        domain: List[str] = self._language.syntax.shift_compound_assignment
        range_checks = self.create_range_checks(
            [
                # OSAA
                self._language.syntax.arithmetic_compound_assignment,
                # OSBA
                self._language.syntax.bitwise_compound_assignment,
                # OSEA
                self._language.syntax.plain_assignment,
            ]
        )
        self.assert_domain_and_ranges(self._compound_assignment_query, domain, range_checks)

    def test_obom_osan_osbn_osrn(self) -> None:
        domain: List[str] = self._language.syntax.shift_operators
        range_checks = self.create_range_checks(
            [
                # OSAN
                self._language.syntax.arithmetic_operators,
                # OSBN
                self._language.syntax.bitwise_operators,
                # OSRN
                self._language.syntax.relational_operators,
            ]
        )
        self.assert_domain_and_ranges(self._binary_expression_query, domain, range_checks)

    def test_mutations(self) -> None:
        program = "a+b;"
        tree = self._parser.parse(program)
        operator_node = tree.root.first_named_child.first_named_child.children[1]
        obom = ObomStrategy(self._parser)
        
        mutations = obom.mutations(
            self._parser,
            tree,
            operator_node
        )
        
        self.assertEqual(operator_node.type, "+")
        self.assertEqual(len(mutations), 13)