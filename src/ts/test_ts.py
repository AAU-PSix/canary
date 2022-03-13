from . import *

import unittest
from importlib.resources import path
from tree_sitter.binding import Query as _Query
from tree_sitter import Language as _Language
from os import path

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
        root: Node = tree.root_node
        self.assertIsInstance(root.type, str)
        self.assertEqual(root.type, "program")

    def test_start_point(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root_node
        point: FilePoint = root.start_point
        self.assertIsInstance(point, FilePoint)
        self.assertEqual(point.line, 0)
        self.assertEqual(point.char, 0)

    def test_start_byte(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root_node
        start_byte: int = root.start_byte
        self.assertIsInstance(start_byte, int)
        self.assertEqual(start_byte, 0)

    def test_end_point(self) -> None:
        tree: Tree = self._parser.parse("console.log(\"Hello, World!\")")
        root: Node = tree.root_node
        point = root.start_point
        self.assertIsInstance(point, FilePoint)
        self.assertEqual(point.line, 0)
        self.assertEqual(point.char, 0)

    def test_end_byte(self) -> None:
        source: int = "console.log(\"Hello, World!\")"
        tree: Tree = self._parser.parse(source)
        root: Node = tree.root_node
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
        root: Node = tree.root_node
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

class TestCapture(unittest.TestCase):
    def test_iterator(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([ node_1, node_2, node_3 ])
        for idx, elem in enumerate(capture):
            self.assertEqual(elem[1], str(idx))

    def test_len(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([ node_1, node_2, node_3 ])
        self.assertEqual(len(capture), 3)

    def test_get(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([ node_1, node_2, node_3 ])
        self.assertEqual(capture[0][1], '0')
        self.assertEqual(capture[1][1], '1')
        self.assertEqual(capture[2][1], '2')

    def test_first(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([ node_1, node_2, node_3 ])
        self.assertEqual(capture.first()[1], '0')

    def test_last(self) -> None:
        node_1: Tuple[Node, str] = (None, '0')
        node_2: Tuple[Node, str] = (None, '1')
        node_3: Tuple[Node, str] = (None, '2')
        capture = Capture([ node_1, node_2, node_3 ])
        self.assertEqual(capture.last()[1], '2')