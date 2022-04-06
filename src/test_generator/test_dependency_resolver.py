import unittest

from symbol_table import (
    SubroutineType,
    PrimitiveType,
    Declaration
)
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
        subroutine = SubroutineType(
            PrimitiveType("void"),
            [
                Declaration(PrimitiveType("int"), "a"),
                Declaration(PrimitiveType("double"), "a")
            ]
        )
        function_declaration = Declaration(subroutine, "foo")
        resolver = DependencyResolver()

        actual: Tuple[List[AstStatement], AstStatement] = resolver.resolve(function_declaration)
        arrange: List[AstStatement] = actual[0]
        arrange_0: AstDeclaration = arrange[0]
        arrange_1: AstDeclaration = arrange[1]
        act: AstExpressionStatement = actual[1]

        self.assertEqual(len(arrange), 2)
        self.assertEqual(arrange_0.identifier, "a_0")
        self.assertEqual(arrange_1.identifier, "a_1")
        self.assertIsInstance(act.epxression, AstFunctionCall)
        self.assertEqual(act.epxression.name, "foo")
        self.assertEqual(len(act.epxression.actual_parameters), 2)