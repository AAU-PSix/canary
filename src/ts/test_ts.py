import unittest
from typing import Tuple, List
from tree_sitter.binding import Query as _Query
from tree_sitter import Language as _Language
from os import path

from ts import CSyntax

from . import FilePoint
from .capture import Capture
from .language_library import Language, LanguageLibrary
from .node import Node
from .parser import Parser
from .query import Query
from .tree import Tree


class TestLanguageLibrary(unittest.TestCase):
    def test_vendor_path(self) -> None:
        self.assertEqual(LanguageLibrary.vendor_path(), './vendor')
        self.assertIsInstance(LanguageLibrary.vendor_path(), str)

    def test_build_path(self) -> None:
        self.assertEqual(LanguageLibrary.build_path(), './build')
        self.assertIsInstance(LanguageLibrary.build_path(), str)

    def test_build_file(self) -> None:
        self.assertEqual(LanguageLibrary.build_file(), 'my-languages.so')
        self.assertIsInstance(LanguageLibrary.build_file(), str)

    def test_full_build_path(self) -> None:
        self.assertEqual(LanguageLibrary.full_build_path(), './build/my-languages.so')
        self.assertIsInstance(LanguageLibrary.full_build_path(), str)

    def test_build(self) -> None:
        LanguageLibrary.build()
        self.assertTrue(path.exists(LanguageLibrary.full_build_path()))
        js = LanguageLibrary.js()
        self.assertIsNotNone(js)
        self.assertIsInstance(js, Language)
        self.assertIsInstance(js._language, _Language)


class TestLanguage(unittest.TestCase):
    _js_language: Language = None

    def setUp(self) -> None:
        LanguageLibrary.build()
        self._js_language = LanguageLibrary.js()
        return super().setUp()

    def test_id(self) -> None:
        self.assertIsNotNone(self._js_language.id)
        self.assertIsInstance(self._js_language.id, int)

    def test_name(self) -> None:
        self.assertIsNotNone(self._js_language.name)
        self.assertEqual(self._js_language.name, 'javascript')
        self.assertIsInstance(self._js_language.name, str)

    def test_field_id_for_name(self) -> None:
        self.assertIsInstance(self._js_language.field_id_for_name('kind'), int)
        self.assertEqual(self._js_language.field_id_for_name('kind'), 21)
        self.assertIsInstance(self._js_language.field_id_for_name('name'), int)
        self.assertEqual(self._js_language.field_id_for_name('name'), 25)
        self.assertIsInstance(self._js_language.field_id_for_name('source'), int)
        self.assertEqual(self._js_language.field_id_for_name('source'), 34)
        self.assertIsInstance(self._js_language.field_id_for_name('condition'), int)
        self.assertEqual(self._js_language.field_id_for_name('condition'), 8)
        self.assertIsInstance(self._js_language.field_id_for_name('consequence'), int)
        self.assertEqual(self._js_language.field_id_for_name('consequence'), 9)
        self.assertIsInstance(self._js_language.field_id_for_name('alternative'), int)
        self.assertEqual(self._js_language.field_id_for_name('alternative'), 2)

    def test_query(self) -> None:
        query = self._js_language.query('(binary_expression (number) (number))')
        self.assertIsInstance(query, Query)
        self.assertIsInstance(query._query, _Query)


class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._parser = Parser.create_with_language(LanguageLibrary.js())
        return super().setUp()

    def test_type(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root
        self.assertIsInstance(root.type, str)
        self.assertEqual(root.type, "program")

    def test_start_point(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root
        point: FilePoint = root.start_point
        self.assertIsInstance(point, FilePoint)
        self.assertEqual(point.line, 0)
        self.assertEqual(point.char, 0)

    def test_start_byte(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root
        start_byte: int = root.start_byte
        self.assertIsInstance(start_byte, int)
        self.assertEqual(start_byte, 0)

    def test_end_point(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root
        point = root.start_point
        self.assertIsInstance(point, FilePoint)
        self.assertEqual(point.line, 0)
        self.assertEqual(point.char, 0)

    def test_end_byte(self) -> None:
        source: int = "console.log(\"Hello, World!\")"
        tree: Tree = self._parser.parse(source)
        root: Node = tree.root
        end_byte: int = root.end_byte
        self.assertIsInstance(end_byte, int)
        self.assertEqual(end_byte, len(source))


class TestTree(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._parser = Parser.create_with_language(LanguageLibrary.js())
        return super().setUp()

    def test_root_node(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root
        self.assertIsInstance(root, Node)


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._parser = Parser.create_with_language(LanguageLibrary.js())
        return super().setUp()

    def test_parse(self) -> None:
        tree: Tree = self._parser.parse("1+2")
        self.assertIsInstance(tree, Tree)

    def test_walk(self) -> None:
        pass

    def test_get_changed_ranges(self) -> None:
        pass


# noinspection DuplicatedCode
class TestCapture(unittest.TestCase):
    def test_iterator(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([node_1, node_2, node_3])
        for idx, elem in enumerate(capture):
            self.assertEqual(elem[1], str(idx))

    def test_len(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([node_1, node_2, node_3])
        self.assertEqual(len(capture), 3)

    def test_get(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([node_1, node_2, node_3])
        self.assertEqual(capture[0][1], '0')
        self.assertEqual(capture[1][1], '1')
        self.assertEqual(capture[2][1], '2')

    def test_first(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([node_1, node_2, node_3])
        self.assertEqual(capture.first()[1], '0')

    def test_last(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([node_1, node_2, node_3])
        self.assertEqual(capture.last()[1], '2')


# noinspection DuplicatedCode
class TestSyntaxForC(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._parser = Parser.c()
        self._language: Language[CSyntax] = self._parser.language
        self._query_function_declaration = self._language.query(
            self._language.syntax.function_declaration_query
        )
        self._query_struct_declaration = self._language.query(
            self._language.syntax.struct_declaration_query
        )

        self._query_if_declaration = self._language.query(
            self._language.syntax.if_statement_query
        )

        return super().setUp()

    def test_no_function_return_empty_list(self):
        root: Node = self._parser.parse(
            "int a = 2"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertIs(len(result), 0)
        self.assertTrue(None not in result)

    def test_single_int_typed_function_gives_single_result(self):
        root: Node = self._parser.parse(
            "int myfunction() {}"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_four_int_typed_function(self):
        root: Node = self._parser.parse(
            "int myfunction1() {} \
             int myfunction2() {} \
             int myfunction3() {} \
             int myfunction4() {}"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
        self.assertTrue(None not in result)

    def test_can_find_int_function_with_single_byte_parameter(self):
        root: Node = self._parser.parse(
            "int myfunction(byte a) { return 0; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_if_statement(self):
        root: Node = self._parser.parse("void iff(){if (a == 2){} return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertTrue(None not in results)

    def test_can_find_two_if_statement(self):
        root: Node = self._parser.parse("void iff(){if (a == 2){} if (a == 2){} return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertTrue(None not in results)

    def test_can_find_if_with_else(self):
        root: Node = self._parser.parse("void iff(){if (a == 2 ) {} else {} return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertTrue(None not in results)

    def test_can_find_if_without_brackets(self):
        root: Node = self._parser.parse("void iff(){if (a == 2 ) return; return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertTrue(None not in results)

    def test_can_find_if_with_else_without_brackets(self):
        root: Node = self._parser.parse("void iff(){if (a == 2 ) return; else return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertTrue(None not in results)

    def test_can_find_no_if_statement(self):
        root: Node = self._parser.parse("void iff(){return;}").root
        capture: Capture = self._query_if_declaration.captures(root)
        results: List[Node] = capture.nodes(self._language.syntax.get_if_declaration)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 0)

    def test_can_find_int_function_with_multiple_byte_parameter(self):
        root: Node = self._parser.parse(
            "int myfunction(byte a, byte b, byte c) { return 1; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_int_function_with_single_char_parameter(self):
        root: Node = self._parser.parse(
            "int myfunction(char a) { return 0;}"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_int_function_with_multiple_char_parameter(self):
        root: Node = self._parser.parse(
            "int myfunction(char a, char b, char c) { return 1; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_void_function_no_parameter(self):
        root: Node = self._parser.parse(
            "void myfunction() { return; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_void_function_with_parameters(self):
        root: Node = self._parser.parse(
            "void myfunction(int a, char b, byte c) { return; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_void_function_with_no_parameters(self):
        root: Node = self._parser.parse(
            "void myfunction() { return; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_can_find_multiple_mixed_type_functions_with_parameters(self):
        root: Node = self._parser.parse(
            "void a() { return; } \
             int b(int c, double d) { return 2; } \
             float e(char f) { return g; }"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertTrue(None not in result)

    def test_can_find_point_return_type(self):
        root: Node = self._parser.parse(
            "int* main() {}"
        ).root
        capture: Capture = self._query_function_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_function_definitions
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_single_struct_dcl_without_identifier(self):
        root: Node = self._parser.parse(
            "struct Books { \
            char title[50]; \
            char author[50]; \
            char subject[100]; \
            int book_id; \
        }").root
        capture: Capture = self._query_struct_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_struct_declaration
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)

    def test_single_struct_dcl_with_identifier(self):
        root: Node = self._parser.parse(
            "struct Books { \
            char title[50]; \
            char author[50]; \
            char subject[100]; \
            int book_id; \
        } myStruct").root
        capture: Capture = self._query_struct_declaration.captures(root)
        result: List[Node] = capture.nodes(
            self._language.syntax.get_struct_declaration
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue(None not in result)
