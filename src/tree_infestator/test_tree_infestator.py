from tree_infestator import TreeInfestator
from cfa import CFA, CFANode, CFAEdge
from ts import language_library, tree_cursor_visitor
from ts.language_library import Language, LanguageLibrary
from ts import Parser, Tree
from unit_analyser import UnitAnalyser
from ts.tree_cursor_visitor import TreeCFAVisitor

from typing import Iterable
import unittest

class TestTreeInfestator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

    def _create_cfa(self, program_string : str) -> TreeInfestator:
        tree = self._parser.parse(program_string)
        CFAVisitor : TreeCFAVisitor = TreeCFAVisitor()
        cfa = CFAVisitor.create(tree.root_node)
        return TreeInfestator(cfa, self._language)
    
    # def test_finds_if_node_in_if_program(self):
    #     infestator = self._create_cfa("if(a==2){a=0;} a = 2;")
    #     self.assertIsNotNone(infestator.sought_nodes)
    #     self.assertEqual(1,len(infestator.sought_nodes))
    





