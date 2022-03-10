from src.ts import LanguageLibrary, Parser, Tree, Node
from .QueryApi import QueryApi
import unittest
from importlib.resources import path
from tree_sitter.binding import Query as _Query
from tree_sitter import Language as _Language
from os import path


class QueryApiTest(unittest.TestCase):

    def setUp(self) -> None:
        LanguageLibrary.build()
        self._c_language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(LanguageLibrary.js())
        self._queryApi = QueryApi()
        return super().setUp()

    # TODO define nodes: One with a single function decl, one with many func. dec., one with none. We also need to
    #  test for different types of functions, to ensure that all types can be handled -- remember structs!!

    def test_no_function_return_empty_list(self):
        tree: Tree = self._parser.parse("int a = 2")
        root: Node = tree.root_node
        self.assertIsNotNone(QueryApi.findFunctionDeclarations(root))
        self.assertIs(len(QueryApi.findFunctionDeclarations(root)), 0)

    




