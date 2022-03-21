from tokenize import Double
import unittest

from . import *

class TestFunctionDeclaration(unittest.TestCase):
    def test_generate_identifier_for_empty(self) -> None:
        resolver = DependencyResolver()
        used_names: Dict[str, int] = dict()
        expected: str = "foo_0"
        actual: str = resolver.generate_identifier_for("foo", used_names)
        self.assertEqual(actual, expected)

    def test_generate_identifier_for_existing(self) -> None:
        resolver = DependencyResolver()
        used_names: Dict[str, int] = {
            "foo": 1
        }
        expected: str = "foo_2"
        actual: str = resolver.generate_identifier_for("foo", used_names)
        self.assertEqual(actual, expected)

    def test_resolve_void_int_int(self) -> None:
        declaration = FunctionDeclaration(
            "foo",
            "void",
            [
                FormalParameter("a", "int"),
                FormalParameter("a", "int"),
            ]
        )
        resolver = DependencyResolver()

        actual: Tuple[List[Statement], Statement] = resolver.resolve(declaration)
        arrange: List[Statement] = actual[0]
        arrange_0: Declaration = arrange[0]
        arrange_1: Declaration = arrange[1]
        act: ExpressionStatement = actual[1]

        self.assertEqual(len(arrange), 2)
        self.assertEqual(arrange_0.identifier, "a_0")
        self.assertEqual(arrange_1.identifier, "a_1")
        self.assertIsInstance(act.epxression, FunctionCall)
        self.assertEqual(act.epxression.name, "foo")
        self.assertEqual(len(act.epxression.actual_parameters), 2)