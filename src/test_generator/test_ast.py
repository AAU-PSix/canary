import unittest

from src.test_generator.ast import FunctionDeclaration
from . import *
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
    Node,
)

class TestFunctionDeclaration(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        return super().setUp()

    def test_create_c(self) -> None:
        tree: Tree = self._parser.parse(
            """
            int add(int a, double b) {
                return a + b;
            }
            """
        )
        function_definition_node: Node = tree.root_node.children[0]
        function_declration: FunctionDeclaration = FunctionDeclaration.create_c(
            tree, function_definition_node
        )
        
        self.assertEqual(function_declration.return_type, "int")
        self.assertEqual(len(function_declration.formal_parameters), 2)
        self.assertEqual(function_declration.formal_parameters[0], "int")
        self.assertEqual(function_declration.formal_parameters[1], "double")