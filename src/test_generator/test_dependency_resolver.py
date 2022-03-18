from tokenize import Double
import unittest

from . import *

class TestFunctionDeclaration(unittest.TestCase):
    def test_reolve_void_int_int(self) -> None:
        declaration = FunctionDeclaration(
            "foo",
            "void",
            [ "int", "int" ]
        )
        resolver = DependencyResolver()
        actual: Tuple[List[Statement], FunctionCall] = resolver.resolve(declaration)
        arrange: List[Statement] = actual[0]
        act: FunctionCall = actual[1]

        self.assertEqual(len(arrange), 2)
        self.assertEqual(arrange[0].lhs, "a")
        self.assertEqual(arrange[1].lhs, "a")
        self.assertEqual(len(act._actual_parameters), 2)
        self.assertEqual(act._actual_parameters[0].value, "a")
        self.assertEqual(act._actual_parameters[1].value, "a")
        
        
    def test_formal_parameter_random_value_double(self) -> None:
        declaration = FunctionDeclaration(
            "foo",
            "void",
            [ "double", "double" ]
        )
        resolver = DependencyResolver()
        actual: Tuple[List[Statement], FunctionCall] = resolver.resolve(declaration)
        arrange: List[Statement] = actual[0]
        act: FunctionCall = actual[1]
        
        first_arrange: Assignment = arrange[0]
        first_arrange_rhs: Constant = first_arrange.rhs
        self.assertEqual(str(float(first_arrange_rhs.value)), first_arrange_rhs.value)
         
    def test_formal_parameter_random_value_int(self) -> None:
        declaration = FunctionDeclaration(
            "foo",
            "void",
            [ "int", "int" ]
        )
        resolver = DependencyResolver()
        actual: Tuple[List[Statement], FunctionCall] = resolver.resolve(declaration)
        arrange: List[Statement] = actual[0]
        act: FunctionCall = actual[1]
        
        first_arrange: Assignment = arrange[0]
        first_arrange_rhs: Constant = first_arrange.rhs
        self.assertEqual(str(int(first_arrange_rhs.value)), first_arrange_rhs.value)        
