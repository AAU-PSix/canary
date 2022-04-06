
from dataclasses import dataclass
from math import factorial
from cfa import (
    CCFAFactory
)
from decorators import *
from cfa.c_cfa_factory import CCFAFactory
from unittest import TestCase
from ts import (
    LanguageLibrary,
    Parser
)

from decorators.location_decorator import LocationDecorator


class TestLocationDecorator(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        return super().setUp()

    def test_single_expression_gets_location_0(self):
                # Step 2: Infest
        program = "a = 2;"
        tree = self._parser.parse(program)


        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root_node)
        decorator = LocationDecorator(cfa)
        result = decorator.decorate()
        nodes = result.cfa.nodes()

        expected = 1
        actual = len(nodes)
        self.assertEqual(actual, expected)
        self.assertTrue(nodes[0].location == 0)
        
  

