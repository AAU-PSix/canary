import unittest

from . import *
from src.ts import LanguageLibrary, Parser

class TestFunctionDeclaration(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        return super().setUp()

    def test_visit_empty_test_case(self) -> None:
        testcase: TestCase = TestCase(
            "hello_world",
            list(),
            None,
            list()
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)

        self.assertEqual(len(lines), 6)
        self.assertEqual(lines[0], "void hello_world(CuTest *ct)")
        self.assertEqual(lines[1], "{")
        self.assertEqual(lines[2], "// Arrange")
        self.assertEqual(lines[3], "// Act")
        self.assertEqual(lines[4], "// Assert")
        self.assertEqual(lines[5], "}")

    def test_visit_empty_test_case_one_arrange(self) -> None:
        arrange_1: Statement = Assignment(
            "foo", Constant("bar")
        )
        testcase: TestCase = TestCase(
            "hello_world",
            [arrange_1],
            None,
            list()
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)

        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], "void hello_world(CuTest *ct)")
        self.assertEqual(lines[1], "{")
        self.assertEqual(lines[2], "// Arrange")
        self.assertEqual(lines[3], "foo = bar;")
        self.assertEqual(lines[4], "// Act")
        self.assertEqual(lines[5], "// Assert")
        self.assertEqual(lines[6], "}")

    def test_visit_empty_test_case_one_arrange_one_act_one_assert(self) -> None:
        arrange: List[Statement] = [
            Declaration("int", "a", Constant("1")),
            Declaration("int", "b", Constant("2")),
            Declaration("int", "expected", Constant("3")),
        ]
        act: Statement = Declaration(
            "int",
            "actual",
            FunctionCall(
                "sum",
                [ Constant("a"), Constant("b") ]
            )
        )
        assertions: List[Assertion] = [
            Assertion(Constant("actual"), Constant("expected"))
        ]
        
        testcase: TestCase = TestCase(
            "test_sum", arrange, act, assertions
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)

        self.assertEqual(len(lines), 11)
        self.assertEqual(lines[0],  "void test_sum(CuTest *ct)")
        self.assertEqual(lines[1],  "{")
        self.assertEqual(lines[2],  "// Arrange")
        self.assertEqual(lines[3],  "int a = 1;")
        self.assertEqual(lines[4],  "int b = 2;")
        self.assertEqual(lines[5],  "int expected = 3;")
        self.assertEqual(lines[6],  "// Act")
        self.assertEqual(lines[7],  "int actual = sum(a, b);")
        self.assertEqual(lines[8],  "// Assert")
        self.assertEqual(lines[9],  "CuAssert(expected, actual);")
        self.assertEqual(lines[10], "}")

    def test_visit_empty_test_case_one_arrange_act(self) -> None:
        arrange_1: Statement = Assignment(
            "foo", Constant("bar")
        )
        act: ExpressionStatement = ExpressionStatement(
            FunctionCall("putin")
        )
        testcase: TestCase = TestCase(
            "hello_world",
            [arrange_1],
            act,
            list()
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)

        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], "void hello_world(CuTest *ct)")
        self.assertEqual(lines[1], "{")
        self.assertEqual(lines[2], "// Arrange")
        self.assertEqual(lines[3], "foo = bar;")
        self.assertEqual(lines[4], "// Act")
        self.assertEqual(lines[5], "putin();")
        self.assertEqual(lines[6], "// Assert")
        self.assertEqual(lines[7], "}")

    def test_visit_empty_test_case__act(self) -> None:
        act: Assignment = Assignment(
            "foo",
            FunctionCall("bar")
        )
        testcase: TestCase = TestCase(
            "hello_world",
            list(),
            act,
            list()
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)

        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], "void hello_world(CuTest *ct)")
        self.assertEqual(lines[1], "{")
        self.assertEqual(lines[2], "// Arrange")
        self.assertEqual(lines[3], "// Act")
        self.assertEqual(lines[4], "foo = bar();")
        self.assertEqual(lines[5], "// Assert")
        self.assertEqual(lines[6], "}")

    def test_generate_for_resolver(self) -> None:
        program: str = "int foo(int bar) { }"
        tree: Tree = self._parser.parse(program)
        function_decl_node: Node = tree.root_node.named_children[0]
        function_decl = FunctionDeclaration.create_c(tree, function_decl_node)
        resolver = DependencyResolver()
        resolution = resolver.resolve(function_decl)
        testcase = TestCase(
            "test",
            resolution[0],
            resolution[1],
            list()
        )
        generator = CuTestCodeGenerator()
        lines: List[str] = generator.visit(testcase)
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], "void test(CuTest *ct)")
        self.assertEqual(lines[1], "{")
        self.assertEqual(lines[2], "// Arrange")
        self.assertTrue(lines[3].startswith("int bar_0 = "), lines[3])
        self.assertTrue(lines[3].endswith(";"), lines[3])
        self.assertEqual(lines[4], "// Act")
        self.assertEqual(lines[5], "int actual = foo(bar_0);")
        self.assertEqual(lines[6], "// Assert")
        self.assertEqual(lines[7], "}")