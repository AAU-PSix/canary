from . import *

import unittest

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

    def test_edit(self) -> None:
        source: str = "1+2"
        tree: Tree = self._parser.parse(source)
        start: int = 0
        length: int = 3
        tree.edit(
            start_byte=start,
            old_end_byte=start,
            new_end_byte=start + length,
            start_point=(0, start),
            old_end_point=(0, start),
            new_end_point=(0, start + length)
        )

        new_source: str = "1+1+2"
        new_tree: Tree = self._parser.parse(new_source, tree)
        self.assertEqual(tree.get_changed_ranges(new_tree), "")

    def test_walk(self) -> None:
        pass

    def test_get_changed_ranges(self) -> None:
        pass