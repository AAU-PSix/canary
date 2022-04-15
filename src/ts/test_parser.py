import unittest
from . import *

class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        return super().setUp()

    def test_replace_a_with_b(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.replace(tree, node_a, "b")
        self.assertEqual(new_tree.text, "b=2;")

    def test_replace_a_with_abc(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.replace(tree, node_a, "abc")
        self.assertEqual(new_tree.text, "abc=2;")

    def test_wrap_prefix(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.wrap(tree, node_a, prefix="b")
        self.assertEqual(new_tree.text, "ba=2;")

    def test_wrap_postfix(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.wrap(tree, node_a, postfix="b")
        self.assertEqual(new_tree.text, "ab=2;")

    def test_wrap_prefix_postfix(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.wrap(tree, node_a, "b", "b")
        self.assertEqual(new_tree.text, "bab=2;")

    def test_insert(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.insert(tree, node_a, "b")
        self.assertEqual(new_tree.text, "ba=2;")

    def test_append(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        node_a: Node = tree.root.children[0].children[0].children[0]
        new_tree: Tree = self._parser.append(tree, node_a, "b")
        self.assertEqual(new_tree.text, "ab=2;")

    def test_insert_line(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        new_tree: Tree = self._parser.insert_line(tree, 0, "b=1;")
        lines: List[str] = new_tree.lines
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "b=1;")
        self.assertEqual(lines[1], "a=2;")

    def test_append_line(self) -> None:
        tree: Tree = self._parser.parse("a=2;")
        new_tree: Tree = self._parser.append_line(tree, 0, "b=1;")
        lines: List[str] = new_tree.lines
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "a=2;")
        self.assertEqual(lines[1], "b=1;")
