from itertools import tee
from tree_infestator import TreeInfestator
from cfa import CFA, CFANode, CFAEdge
from ts import language_library, tree_cursor_visitor
from ts.language_library import Language, LanguageLibrary
from ts import Parser, Tree
from unit_analyser import UnitAnalyser
from ts.tree_cursor_visitor import TreeCFAVisitor

from typing import Iterable
import string
import unittest

class TestTreeInfestator(unittest.TestCase):

    @staticmethod
    def removeWhitespace(input:str):
        return input.translate(str.maketrans('', '', string.whitespace))


    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

    def _create_cfa(self, program_string : str) -> TreeInfestator:
        self.tree = self._parser.parse(program_string)
        CFAVisitor : TreeCFAVisitor = TreeCFAVisitor(self.tree)
        cfa = CFAVisitor.create(self.tree.root_node)
        return TreeInfestator(cfa, self._parser)
    
    def test_finds_if_node_in_if_program(self):
        infestator = self._create_cfa("if(a==2){a=0;} a = 2;")
        self.assertIsNotNone(infestator.found_nodes)
        self.assertEqual(1,len(infestator.found_nodes))
    
    def test_finds_several_if_nodes_in_if_program(self):
        infestator = self._create_cfa("if(a==2){a=0;} a = 2; if(b==3){hest = 3;}")
        self.assertIsNotNone(infestator.found_nodes)
        self.assertEqual(2,len(infestator.found_nodes))

    def test_found_nodes_are_reversed_correctly(self):
        infestator = self._create_cfa("if(a==2){a=0;} a = 2; if(b==3){hest = 3;}")
        self.assertIsNotNone(infestator.found_nodes)
        nodes : list(CFANode) = infestator.found_nodes
        previous = nodes[0].node.start_byte
        otherNode = nodes[1].node.start_byte
        self.assertGreater(previous, otherNode)


    def test_found_nested_nodes_are_reversed_correctly(self):
        infestator = self._create_cfa("if(a==2){a=0; if(ko == 2){gris = 1;}} a = 2; if(b==3){hest = 3;}")
        self.assertIsNotNone(infestator.found_nodes)
        nodes : list(CFANode) = infestator.found_nodes
        first = nodes[0].node.start_byte
        second = nodes[1].node.start_byte
        third = nodes[2].node.start_byte
        self.assertGreater(first, second)
        self.assertGreater(first, third)
        self.assertGreater(second, third)
            
    def test_found_no_if_nodes_in_program(self):
        infestator = self._create_cfa("int main(){a=2;}")
        self.assertIsNotNone(infestator.found_nodes)
        self.assertEqual(0,len(infestator.found_nodes))


    def test_can_infest_if_statement_with_newlines(self):
        infestator = self._create_cfa("if(a==2)\n{ a=2;\n}")
        t = infestator.infest_tree(self.tree)
        self.assertTrue("TWEET();" in t.text)

    def test_can_infest_if_statement_without_newlines(self):
        inputStr = "if(a==2){ a=2;\n}"
        infestator = self._create_cfa(inputStr)
        t = infestator.infest_tree(self.tree)

        expected = self.removeWhitespace("if(a==2)\n{ TWEET(); a=2;\n}")
        actual = self.removeWhitespace(t.text)
        print(actual)
        print(expected)
        self.assertEqual(actual,expected)



