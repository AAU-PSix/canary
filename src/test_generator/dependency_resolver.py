from typing import List, Tuple
from .ast import Assignment, Constant, Expression, FunctionCall, FunctionDeclaration, Statement
import random

class DependencyResolver:
    def __init__(self) -> None:
        pass

    def resolve(self, function: FunctionDeclaration) -> Tuple[List[Statement], FunctionCall]:
        arrange: List[Statement] = list()
        parameters: List[Expression] = list()

        for parameter in function.formal_parameters:
            if parameter == "int" or parameter == "double":
                
                arrange.append(Assignment("a", self.formal_parameter_random_value(parameter)))
                parameters.append(Constant("a"))

        return (arrange, FunctionCall(function.name, parameters))
    
    def formal_parameter_random_value(self, type: str) -> Constant:
        if type == "int":
            random_int_value = str(random.randint(0, 100))
            return Constant(random_int_value)
        
        if type == "double":
            random_double_value = str(random.uniform(0, 100))
            return Constant(random_double_value)
        
        return None 
    
    
    