import unittest

from src.ts import *
from src.cfa import *
from . import TreeInfestator

class TestTreeInfestator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._infestator = TreeInfestator(self._parser)

    def test_is_condition_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        condition: Node = if_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._infestator.is_condition_of_if(condition)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        alternative: Node = if_node.child_by_field_name("alternative")
        expected: bool = False

        actual = self._infestator.is_condition_of_if(alternative)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(alternative.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_consequence_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        consequence: Node = if_node.child_by_field_name("consequence")
        expected: bool = True

        actual = self._infestator.is_consequence_of_if(consequence)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(consequence.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_consequence_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        consequence: Node = if_node.child_by_field_name("alternative")
        expected: bool = False

        actual = self._infestator.is_consequence_of_if(consequence)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(consequence.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_alternative_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        alternative: Node = if_node.child_by_field_name("alternative")
        expected: bool = True

        actual = self._infestator.is_alternative_of_if(alternative)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(alternative.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_alternative_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        consequence: Node = if_node.child_by_field_name("consequence")
        expected: bool = False

        actual = self._infestator.is_alternative_of_if(consequence)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(consequence.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_sorted_cfa(self) -> None:
        program: str = "if(a) { } else { a=2; }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
        sorted: List[CFANode] = self._infestator.sorted_cfa(cfa)

        self.assertEqual(len(sorted), 3)
        self.assertEqual(sorted[0].node.type, "expression_statement")
        self.assertEqual(sorted[1].node.type, "compound_statement")
        self.assertEqual(sorted[2].node.type, "parenthesized_expression")


    def test_infect(self) -> None:
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
        actual: Tree = self._infestator.infect(tree, cfa)
        self.assertEqual(actual.text, "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }")

    def test_else_if_is_alternative_of_if_false(self) -> None:
        program: str = "if(a) { } else if (b){ }"
        tree: Tree = self._parser.parse(program)
        if_else_node: Node = tree.root_node.named_children[0]
        consequence: Node = if_else_node.child_by_field_name("consequence")
        
        expected: bool = False
        actual = self._infestator.is_alternative_of_if(consequence)

        self.assertEqual(if_else_node.type, "if_statement")
        self.assertEqual(consequence.type, "compound_statement")
        self.assertEqual(actual, expected)


    def test_else_if_else_is_alternative_of_if_false(self) -> None:
        program: str = "if(a) { } else if (b){ } else {}"
        tree: Tree = self._parser.parse(program)
        else_if_else_node: Node = tree.root_node.named_children[0]

        consequence: Node = else_if_else_node.child_by_field_name("consequence")
        
        expected: bool = True
        actual = self._infestator.is_consequence_of_if(consequence)
        
        self.assertEqual(else_if_else_node.type, "if_statement")
        self.assertEqual(consequence.type, "compound_statement")
        self.assertEqual(actual, expected)  


    def test_can_add_tweet_for_if_statement(self):
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); }"
        self.assertEqual(expected, actual)

#    def test_can_add_tweets_for_sequential_if_statement(self):
#        program: str = "if(a) { } if (b) { }"
#        tree: Tree = self._parser.parse(program)
#
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#
#        actual = self._infestator.infect(tree, cfa).text
#        expected = "if(a) {TWEET(); } if (b) {TWEET(); }"
#        self.assertEqual(expected, actual)
#
#    def test_can_add_tweets_for_nested_if_statements(self):
#        program: str = "if(a) { if (b) { } }"
#        tree: Tree = self._parser.parse(program)
#
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#
#        actual = self._infestator.infect(tree, cfa).text
#        expected = "if(a) {TWEET(); if (b) {TWEET(); }}"
#        self.assertEqual(expected, actual)
#
#    def test_can_add_tweets_for_if_with_nested_else(self):
#        program: str = "if(a) { if (b) { } } else {}"
#        tree: Tree = self._parser.parse(program)
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#
#        actual = self._infestator.infect(tree, cfa).text
#        expected = "if(a) {TWEET(); if (b) {TWEET(); } } else {TWEET();}"
#        self.assertEqual(expected, actual)
#
#    def test_can_add_tweets_for_if_with_nested_else_with_if(self):
#        program: str = "if(a) { if (b) { } } else { if (a){}}"
#        tree: Tree = self._parser.parse(program)
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#
#        actual = self._infestator.infect(tree, cfa).text
#        expected = "if(a) {TWEET(); if (b) {TWEET(); } } else {TWEET(); if (a){TWEET();}}"
#        self.assertEqual(expected, actual)
#
#    def test_can_add_tweets_for_if_elif_else(self):
#        program: str = "if(a) { } else if (b) {} else if (c) {} else {}"
#        tree: Tree = self._parser.parse(program)
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#
#        actual = self._infestator.infect(tree, cfa).text
#        expected = "if(a) {TWEET(); } else if (b) {TWEET();} else if (c) {TWEET();} else {TWEET();}"
#        self.assertEqual(expected, actual)        
#
#    def _create_and_infect_tree(self,program:str) -> str:
#        tree: Tree = self._parser.parse(program)
#        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node.first_child, False)
#        return self._infestator.infect(tree, cfa).text
#
#
#    def test_can_add_tweets_for_if_elif_elif_else(self):
#        actual = self._create_and_infect_tree("if(a) { } else if (b) {} else if (c) {} else {}")        
#        expected = "if(a) {TWEET(); } else if (b) {TWEET();} else if (c) {TWEET();} else {TWEET();}"
#        self.assertEqual(expected, actual)       
#
#    def test_can_add_tweets_for_if_elif_elif_nested_if_else(self):
#        actual = self._create_and_infect_tree("if(a) { } else if (b) {} else if (c) { if (a) {} else if (b) {}} else {}")        
#        expected = "if(a) {TWEET(); } else if (b) {TWEET();} else if (c) {TWEET(); if (a) {TWEET();} else if (b) {TWEET();}} else {TWEET();}"
#        self.assertEqual(expected, actual)        
    







