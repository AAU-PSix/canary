import unittest
from . import *

class TestTree(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.query_compound_assignment)
        self._assignment_query: Query = self._language.query(self._language.syntax.query_assignment)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.query_binary_expression)
        return super().setUp()

#    def test_replace_singlechar_with_two(self) -> None:
#        tree: Tree = self._parser.parse("1+2")
#        binary_expression_capture: Capture = self._language.query(
#            self._language.syntax._binary_expression_query
#        ).captures(tree.root_node)
#        binary_expression_operator_nodes: List[Node] = binary_expression_capture.nodes(
#            self._language.syntax.get_binary_expression_operator
#        )
#        operator_node: Node = binary_expression_operator_nodes[0]
#
#        new_tree: Tree = tree.replace(self._parser, operator_node, ">>")
#
#        self.assertEqual(len(binary_expression_operator_nodes), 1)
#        self.assertEqual(new_tree.text, "1>>2")