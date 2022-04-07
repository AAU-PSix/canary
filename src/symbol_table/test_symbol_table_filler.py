from unittest import TestCase
from ts import LanguageLibrary, Parser, CSyntax
from .declaration import Declaration
from .types.primitive_type import PrimitiveType
from .types.subroutine_type import SubroutineType
from . import *

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

    def test_type_struct(self) -> None:
        program = """
            struct Foo {
                int foo1;
            };
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 1)
        self.assertTrue("struct Foo" in root_identifiers)
        
        foo: CDeclaration = root_table.lookup("struct Foo")
        foo_type: CompositeType = foo.type
        self.assertIsInstance(foo_type, CompositeType)
        self.assertEqual(len(foo_type.composition), 1)
        self.assertEqual(foo_type.composition[0].identifier, "foo1")
        self.assertIsInstance(foo_type.composition[0].member, PrimitiveType)

    def test_type_union(self) -> None:
        program = """
            union Foo {
                int foo1;
            };
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 1)
        self.assertTrue("union Foo" in root_identifiers)

        foo: CDeclaration = root_table.lookup("union Foo")
        foo_type: CompositeType = foo.type
        self.assertIsInstance(foo, CDeclaration)
        self.assertIsInstance(foo_type, CompositeType)
        self.assertEqual(len(foo_type.composition), 1)
        self.assertEqual(foo_type.composition[0].identifier, "foo1")
        self.assertIsInstance(foo_type.composition[0].member, PrimitiveType)

    def test_type_enum(self) -> None:
        program = """
            enum Foo {
                Failed = 0,
                Working,
            };
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 1)
        self.assertTrue("enum Foo" in root_identifiers)

        foo: CDeclaration = root_table.lookup("enum Foo")
        foo_type: EnumType = foo.type
        self.assertIsInstance(foo_type, EnumType)
        self.assertEqual(len(foo_type.enumerators), 2)
        self.assertEqual(foo_type.enumerators[0].identifier, "Failed")
        self.assertEqual(foo_type.enumerators[0].value, 0)
        self.assertEqual(foo_type.enumerators[1].identifier, "Working")
        self.assertEqual(foo_type.enumerators[1].value, None)

    def test_type_definition(self) -> None:
        program = """
            struct Foo {
                int foo1;
            };
            
            typedef struct Foo Bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("struct Foo" in root_identifiers)
        self.assertTrue("Bar" in root_identifiers)

        foo_type: CompositeType = root_table.lookup("struct Foo").type
        self.assertIsInstance(foo_type, CompositeType)
        self.assertEqual(len(foo_type.composition), 1)
        self.assertEqual(foo_type.composition[0].identifier, "foo1")
        self.assertIsInstance(foo_type.composition[0].member, PrimitiveType)

        bar_type: CDeclaration = root_table.lookup("Bar")
        self.assertEqual(foo_type, bar_type.type)

    def test_type_definition_struct(self) -> None:
        program = """
            typedef struct Foo {
                int foo1;
            } Bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("struct Foo" in root_identifiers)
        
        foo_type: CompositeType = root_table.lookup("struct Foo").type
        self.assertIsInstance(foo_type, CompositeType)
        self.assertEqual(len(foo_type.composition), 1)
        self.assertEqual(foo_type.composition[0].identifier, "foo1")
        self.assertIsInstance(foo_type.composition[0].member, PrimitiveType)

        bar_type: CDeclaration = root_table.lookup("Bar")
        self.assertEqual(foo_type, bar_type.type)

    def test_type_definition_union(self) -> None:
        program = """
            typedef union Foo {
                int foo1;
            } Bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("union Foo" in root_identifiers)
        
        foo_type: CompositeType = root_table.lookup("union Foo").type
        self.assertIsInstance(foo_type, CompositeType)
        self.assertEqual(len(foo_type.composition), 1)
        self.assertEqual(foo_type.composition[0].identifier, "foo1")
        self.assertIsInstance(foo_type.composition[0].member, PrimitiveType)

        bar_type: CDeclaration = root_table.lookup("Bar")
        self.assertEqual(foo_type, bar_type.type)

    def test_type_definition_enum(self) -> None:
        program = """
            typedef enum Foo {
                Failed = 0,
                Working,
            } Bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("enum Foo" in root_identifiers)

        foo_type: EnumType = root_table.lookup("enum Foo").type
        self.assertIsInstance(foo_type, EnumType)
        self.assertEqual(len(foo_type.enumerators), 2)
        self.assertEqual(foo_type.enumerators[0].identifier, "Failed")
        self.assertEqual(foo_type.enumerators[0].value, 0)
        self.assertEqual(foo_type.enumerators[1].identifier, "Working")
        self.assertEqual(foo_type.enumerators[1].value, None)

        bar_type: CDeclaration = root_table.lookup("Bar")
        self.assertEqual(foo_type, bar_type.type)

    def test_declaration_primitive(self) -> None:
        program = """
            int foo = 0;
            int bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("foo" in root_identifiers)
        self.assertTrue("bar" in root_identifiers)

        foo_type: PrimitiveType = root_table.lookup("foo").type
        self.assertIsInstance(foo_type, PrimitiveType)
        self.assertEqual(foo_type.name, "int")
        bar_type: PrimitiveType = root_table.lookup("bar").type
        self.assertIsInstance(bar_type, PrimitiveType)
        self.assertEqual(bar_type.name, "int")
        self.assertEqual(foo_type, bar_type)

    def test_declaration_with_storage_class_specifier(self) -> None:
        program = """
            static int foo = 0;
            static int bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("foo" in root_identifiers)
        self.assertTrue("bar" in root_identifiers)

        foo: CDeclaration = root_table.lookup("foo")
        foo_type: PrimitiveType = foo.type
        self.assertIsInstance(foo_type, PrimitiveType)
        self.assertEqual(foo_type.name, "int")
        self.assertEqual(len(foo.type_qualifiers), 0)
        self.assertEqual(len(foo.storage_class_specifiers), 1)
        self.assertTrue("static" in foo.storage_class_specifiers)
        
        bar: CDeclaration = root_table.lookup("bar")
        bar_type: PrimitiveType = bar.type
        self.assertIsInstance(bar_type, PrimitiveType)
        self.assertEqual(bar_type.name, "int")
        self.assertEqual(len(bar.type_qualifiers), 0)
        self.assertEqual(len(bar.storage_class_specifiers), 1)
        self.assertTrue("static" in bar.storage_class_specifiers)

        self.assertEqual(foo_type, bar_type)

    def test_declaration_with_type_qualifier(self) -> None:
        program = """
            const int foo = 0;
            const int bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("foo" in root_identifiers)
        self.assertTrue("bar" in root_identifiers)

        foo: CDeclaration = root_table.lookup("foo")
        foo_type: PrimitiveType = foo.type
        self.assertIsInstance(foo_type, PrimitiveType)
        self.assertEqual(foo_type.name, "int")
        self.assertEqual(len(foo.storage_class_specifiers), 0)
        self.assertEqual(len(foo.type_qualifiers), 1)
        self.assertTrue("const" in foo.type_qualifiers)
        
        bar: CDeclaration = root_table.lookup("bar")
        bar_type: PrimitiveType = bar.type
        self.assertIsInstance(bar_type, PrimitiveType)
        self.assertEqual(bar_type.name, "int")
        self.assertEqual(len(bar.storage_class_specifiers), 0)
        self.assertEqual(len(bar.type_qualifiers), 1)
        self.assertTrue("const" in bar.type_qualifiers)

    def test_declaration_with_storage_class_specifier_and_type_qualifier(self) -> None:
        program = """
            static const int foo = 0;
            static const int bar;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        root_identifiers = root_table.identifiers()
        self.assertEqual(len(root_identifiers), 2)
        self.assertTrue("foo" in root_identifiers)
        self.assertTrue("bar" in root_identifiers)

        foo: CDeclaration = root_table.lookup("foo")
        foo_type: PrimitiveType = foo.type
        self.assertIsInstance(foo_type, PrimitiveType)
        self.assertEqual(foo_type.name, "int")
        self.assertEqual(len(foo.storage_class_specifiers), 1)
        self.assertTrue("static" in foo.storage_class_specifiers)
        self.assertEqual(len(foo.type_qualifiers), 1)
        self.assertTrue("const" in foo.type_qualifiers)
        
        bar: CDeclaration = root_table.lookup("bar")
        bar_type: PrimitiveType = bar.type
        self.assertIsInstance(bar_type, PrimitiveType)
        self.assertEqual(bar_type.name, "int")
        self.assertEqual(len(bar.storage_class_specifiers), 1)
        self.assertTrue("static" in bar.storage_class_specifiers)
        self.assertEqual(len(bar.type_qualifiers), 1)
        self.assertTrue("const" in bar.type_qualifiers)

    def test_declaration_array(self) -> None:
        program = """
            int foo[];
            int bar[const 100];
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        foo: CDeclaration = root_table.lookup("foo")
        foo_type: CAggregateType = foo.type
        self.assertIsInstance(foo_type, CAggregateType)

        bar: CDeclaration = root_table.lookup("bar")
        bar_type: CAggregateType = bar.type
        self.assertIsInstance(bar_type, CAggregateType)

    def test_pointers(self) -> None:
        program = """
            int *a, **b, ***c;
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root

        a: CDeclaration = root_table.lookup("a")
        a_type: CPointerType = a.type
        self.assertIsInstance(a_type, CPointerType)
        self.assertEqual(a_type.multiple_indirection, 1)

        b: CDeclaration = root_table.lookup("b")
        b_type: CPointerType = b.type
        self.assertIsInstance(b_type, CPointerType)
        self.assertEqual(b_type.multiple_indirection, 2)

        c: CDeclaration = root_table.lookup("c")
        c_type: CPointerType = c.type
        self.assertIsInstance(c_type, CPointerType)
        self.assertEqual(c_type.multiple_indirection, 3)

    def test_functions_1(self) -> None:
        program = """
            int Foo1(int *a) { }
            void Foo2(int *a, int b) { }
            void Foo3() { }
        """
        tree = self._parser.parse(program)

        root_table = self._filler.fill(tree).root
        
        foo1 = root_table.lookup("Foo1")
        foo1_type: SubroutineType[Declaration] = foo1.type
        self.assertIsInstance(foo1_type, SubroutineType)
        self.assertEqual(foo1_type.arity, 1)
        self.assertIsInstance(foo1_type.parameters[0].type, CPointerType)

        foo2 = root_table.lookup("Foo2")
        foo2_type: SubroutineType[Declaration] = foo2.type
        self.assertIsInstance(foo2_type, SubroutineType)
        self.assertEqual(foo2_type.arity, 2)
        self.assertIsInstance(foo2_type.parameters[0].type, CPointerType)
        self.assertIsInstance(foo2_type.parameters[1].type, PrimitiveType)

        foo3 = root_table.lookup("Foo3")
        foo3_type: SubroutineType[Declaration] = foo3.type
        self.assertIsInstance(foo3_type, SubroutineType)
        self.assertEqual(foo3_type.arity, 0)