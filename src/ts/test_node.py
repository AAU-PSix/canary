import unittest
from . import *

class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        return super().setUp()

    def test_is_immediate_descendt_of_type_for_statement(self) -> None:
        program: str = "for(;;) { a=1; }"
        tree: Tree = self._parser.parse(program)
        # "a=1;"
        expression_stmt: Node = tree.root \
            .first_named_child.first_named_child.first_named_child

        expected: bool = True
        actual = expression_stmt.is_immediate_descendt_of_type("for_statement")

        self.assertEqual(actual, expected)
    
    def test(self) -> None:
        program: str = "for(;;) { a=1; }"
        tree: Tree = self._parser.parse(program)
        for_stmt: Node = tree.root.first_named_child
        # "a=1;"
        expression_stmt: Node = for_stmt \
            .first_named_child.first_named_child
        types: List[str] = [
            "if_statement",
            "while_statement",
            "do_statement",
            "for_statement",
            "switch_statement",
        ]

        expected: str = for_stmt
        actual = expression_stmt.get_immediate_descendent_of_types(types)

        self.assertEqual(actual, expected)