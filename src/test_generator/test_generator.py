import unittest

from . import *
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
    Node
)

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
        generator = CuTestSuiteCodeGenerator()
        lines: List[str] = generator.visit_test_case(testcase)

        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0].strip(), "void hello_world(CuTest *ct) {")
        self.assertEqual(lines[1].strip(), "// Arrange")
        self.assertEqual(lines[2].strip(), "// Act")
        self.assertEqual(lines[3].strip(), "// Assert")
        self.assertEqual(lines[4].strip(), "}")

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
        generator = CuTestSuiteCodeGenerator()
        lines: List[str] = generator.visit_test_case(testcase)

        self.assertEqual(len(lines), 6)
        self.assertEqual(lines[0].strip(), "void hello_world(CuTest *ct) {")
        self.assertEqual(lines[1].strip(), "// Arrange")
        self.assertEqual(lines[2].strip(), "foo = bar;")
        self.assertEqual(lines[3].strip(), "// Act")
        self.assertEqual(lines[4].strip(), "// Assert")
        self.assertEqual(lines[5].strip(), "}")

#    def test_visit_empty_test_case_one_arrange_one_act_one_assert(self) -> None:
#        arrange: List[Statement] = [
#            Declaration("int", "a", Constant("1")),
#            Declaration("int", "b", Constant("2")),
#            Declaration("int", "expected", Constant("3")),
#        ]
#        act: Statement = Declaration(
#            "int",
#            "actual",
#            FunctionCall(
#                "sum",
#                [ Constant("a"), Constant("b") ]
#            )
#        )
#        assertions: List[Assertion] = [
#            Assertion(Constant("actual"), Constant("expected"))
#        ]
#        
#        testcase: TestCase = TestCase(
#            "test_sum", arrange, act, assertions
#        )
#        generator = CuTestSuiteCodeGenerator()
#        lines: List[str] = generator.visit_test_case(testcase)
#
#        self.assertEqual(len(lines), 10)
#        self.assertEqual(lines[0].strip(), "void test_sum(CuTest *ct) {")
#        self.assertEqual(lines[1].strip(), "// Arrange")
#        self.assertEqual(lines[2].strip(), "int a = 1;")
#        self.assertEqual(lines[3].strip(), "int b = 2;")
#        self.assertEqual(lines[4].strip(), "int expected = 3;")
#        self.assertEqual(lines[5].strip(), "// Act")
#        self.assertEqual(lines[6].strip(), "CANARY_ACT(int actual = sum(a, b););")
#        self.assertEqual(lines[7].strip(), "// Assert")
#        self.assertEqual(lines[8].strip(), "CuAssert(expected, actual);")
#        self.assertEqual(lines[9].strip(), "}")

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
        generator = CuTestSuiteCodeGenerator()
        lines: List[str] = generator.visit_test_case(testcase)

        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0].strip(), "void hello_world(CuTest *ct) {")
        self.assertEqual(lines[1].strip(), "// Arrange")
        self.assertEqual(lines[2].strip(), "foo = bar;")
        self.assertEqual(lines[3].strip(), "// Act")
        self.assertEqual(lines[4].strip(), "CANARY_ACT(putin(););")
        self.assertEqual(lines[5].strip(), "// Assert")
        self.assertEqual(lines[6].strip(), "}")

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
        generator = CuTestSuiteCodeGenerator()
        lines: List[str] = generator.visit_test_case(testcase)

        self.assertEqual(len(lines), 6)
        self.assertEqual(lines[0].strip(), "void hello_world(CuTest *ct) {")
        self.assertEqual(lines[1].strip(), "// Arrange")
        self.assertEqual(lines[2].strip(), "// Act")
        self.assertEqual(lines[3].strip(), "CANARY_ACT(foo = bar(););")
        self.assertEqual(lines[4].strip(), "// Assert")
        self.assertEqual(lines[5].strip(), "}")

    # def test_generate_for_resolver(self) -> None:
    #     program: str = "int foo(int bar) { }"
    #     tree: Tree = self._parser.parse(program)
    #     function_decl_node: Node = tree.root_node.named_children[0]
    #     function_decl = FunctionDeclaration.create_c(tree, function_decl_node)
    #     resolver = DependencyResolver()
    #     resolution = resolver.resolve(function_decl)
    #     testcase = TestCase(
    #         "test",
    #         resolution[0],
    #         resolution[1],
    #         list()
    #     )
    #     generator = CuTestSuiteCodeGenerator()
    #     lines: List[str] = generator.visit_test_case(testcase)
    #     self.assertEqual(len(lines), 7)
    #     self.assertEqual(lines[0].strip(), "void test(CuTest *ct) {")
    #     self.assertEqual(lines[1].strip(), "// Arrange")
    #     self.assertTrue(lines[2].strip().startswith("int bar_0 = "), lines[3])
    #     self.assertTrue(lines[2].strip().endswith(";"), lines[3])
    #     self.assertEqual(lines[3].strip(), "// Act")
    #     self.assertEqual(lines[4].strip(), "CANARY_ACT(int actual = foo(bar_0););")
    #     self.assertEqual(lines[5].strip(), "// Assert")
    #     self.assertEqual(lines[6].strip(), "}")