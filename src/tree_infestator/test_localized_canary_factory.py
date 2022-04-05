from typing import List, Tuple
import unittest
from src.tree_infestator.localized_canary_factory import LocalisedTree
from src.ts.tree_cursor import TreeCursor
from ts import (
    LanguageLibrary,
    Tree,
    Node,
    Parser,
    CSyntax,
    CField,
)
from cfa import (
    CFA,
    CCFAFactory
)
from .test_tree_infestator import TestTreeInfestator
from . import LocalisedCCanaryFactory, LocalisedCInfestator

class TestLocalizedTreeInfestator(TestTreeInfestator):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._factory = LocalisedCCanaryFactory()
        self._infestator = LocalisedCInfestator(self._parser, self._factory)
        self._syntax = CSyntax()
        self._tree_pointer = TreeCursor

    @staticmethod
    def _count_locations(tree: LocalisedTree) -> int:
        print (tree)
        return 0
  
    def test_adds_locations_to_expected_number_of_nodes_while_1(self):
        # We expect there to be two locations initially --- one before while and 
        # one inside the while.
        program: str = "a = 2; while(a) { a = 3; }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = CCFAFactory(tree).create(tree.root_node)

        tree = self._infestator.infect(tree, cfa)
        expected = 2
        actual = self._count_locations(tree)
        self.assertEqual(expected, actual)

    def test_adds_locations_to_expected_number_of_nodes_while_2(self):
        # We expect there to be two locations initially --- one before and after while (the same location)
        # and one inside the while.
        program: str = "a = 2; while(a) { a = 3; } a = 4;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = CCFAFactory(tree).create(tree.root_node)

        tree = self._infestator.infect(tree, cfa)
        
        expected = 2
        actual = self._count_locations(tree)
        self.assertEqual(expected, actual)
        self.assertEqual(len(self._factory.new_locations), actual)
    
    def test_adds_locations_to_expected_number_of(self):
        # We expect there to be two locations initially --- one before and after while (the same location)
        # and one inside the while.
        program: str = "a = 2; while(a) { a = 3; } a = 4;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = CCFAFactory(tree).create(tree.root_node)

        tree = self._infestator.infect(tree, cfa)
        
        expected = 2
        actual = self._count_locations(tree)
        self.assertEqual(expected, actual)
        self.assertEqual(len(self._factory.new_locations), actual)

        

    

    


        
        
    