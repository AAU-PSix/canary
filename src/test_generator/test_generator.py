import unittest

from . import *

class TestFunctionDeclaration(unittest.TestCase):
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
        self.assertEqual(lines[3], "foo=bar;")
        self.assertEqual(lines[4], "// Act")
        self.assertEqual(lines[5], "// Assert")
        self.assertEqual(lines[6], "}")

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
        self.assertEqual(lines[3], "foo=bar;")
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
        self.assertEqual(lines[4], "foo=bar();")
        self.assertEqual(lines[5], "// Assert")
        self.assertEqual(lines[6], "}")