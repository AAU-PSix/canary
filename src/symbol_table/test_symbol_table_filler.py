from unittest import TestCase
from ts import LanguageLibrary, Parser, CSyntax
from .symbol_table_filler import CSymbolTableFiller

class TestSymbolTableFiller(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._syntax = CSyntax()
        self._filler = CSymbolTableFiller(self._syntax)

    def test_fill_symbol_table_single_scope_and_declaration(self) -> None:
        program = """
            int foo = 1;
            int bar = 2;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        self.assertEqual(root_table.child_count, 0)
        identifiers = root_table.identifiers()
        self.assertEqual(len(identifiers), 2)
        self.assertTrue("foo" in identifiers)
        self.assertTrue("bar" in identifiers)

    def test_fill_symbol_table_single_nested_scope_and_declaration(self) -> None:
        program = """
            int foo = 1;
            {
                int bar = 2;
            }
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        self.assertEqual(root_table.child_count, 1)
        identifiers_0 = root_table.identifiers()
        self.assertEqual(len(identifiers_0), 1)
        self.assertTrue("foo" in identifiers_0)

        identifiers_1 = root_table.children[0].identifiers()
        self.assertEqual(len(identifiers_1), 2)
        self.assertTrue("bar" in identifiers_1)
        self.assertTrue("bar" in identifiers_1)

    def test_fill_symbol_table_simple_function(self) -> None:
        program = """
            int Foo(int bar) {
                return bar * bar;
            }
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 1)
        self.assertTrue("Foo" in root_identifiers)

        self.assertEqual(root_table.child_count, 1)
        function_scope = root_table.children[0]
        function_identifiers = function_scope.identifiers()
        self.assertEqual(len(function_identifiers), 2)
        self.assertTrue("Foo" in function_identifiers)
        self.assertTrue("bar" in function_identifiers)