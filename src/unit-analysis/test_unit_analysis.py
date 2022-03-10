from src.ts import LanguageLibrary, Parser, Tree, Node
from .QueryApi import QueryApi
import unittest


class QueryApiTest(unittest.TestCase):

    def setUp(self) -> None:
        LanguageLibrary.build()
        self._c_language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(LanguageLibrary.c())
        self._queryApi = QueryApi()
        return super().setUp()

    # TODO define nodes: One with a single function decl, one with many func. dec., one with none. We also need to
    #  test for different types of functions, to ensure that all types can be handled -- remember structs!!

    def test_no_function_return_empty_list(self):
        tree: Tree = self._parser.parse("int a = 2")
        root: Node = tree.root_node
        self.assertIsNotNone(QueryApi.findFunctionDeclarations(root))
        self.assertIs(len(QueryApi.findFunctionDeclarations(root)), 0)

    def test_single_int_typed_function_gives_single_result(self):
        tree: Tree = self._parser.parse("int myfunction() {}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_four_int_typed_function(self):
        tree: Tree = self._parser.parse(
            "int myfunction1() {}int myfunction2() {}int myfunction3() {}int myfunction4() {}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)

    def test_can_find_int_function_with_single_byte_parameter(self):
        tree: Tree = self._parser.parse("int myfunction(byte a) { return 0;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_int_function_with_multiple_byte_parameter(self):
        tree: Tree = self._parser.parse("int myfunction(byte a, byte b, byte c) {return 1;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_int_function_with_single_char_parameter(self):
        tree: Tree = self._parser.parse("int myfunction(char a) { return 0;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_int_function_with_multiple_char_parameter(self):
        tree: Tree = self._parser.parse("int myfunction(char a, char b, char c) {return 1;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_void_function_no_parameter(self):
        tree: Tree = self._parser.parse("void myfunction() {return;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_void_function_with_parameters(self):
        tree: Tree = self._parser.parse("void myfunction(int a, char b, byte c) {return;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_void_function_with_no_parameters(self):
        tree: Tree = self._parser.parse("void myfunction() {return;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_can_find_multiple_mixed_type_functions_with_parameters(self):
        tree: Tree = self._parser.parse("void a() {return;} int b(int c, double d) {return 2;} float e(char f) {"
                                        "return g;}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)


    def test_can_find_point_return_type(self):
        tree: Tree = self._parser.parse("int* main(){}")
        root: Node = tree.root_node
        result = QueryApi.findFunctionDeclarations(root)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
