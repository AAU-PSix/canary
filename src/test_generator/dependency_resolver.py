from typing import Dict, List, Tuple
import random

from symbol_table import (
    Declaration,
    SubroutineType,
    PrimitiveType
)
from .ast_statement import Statement as AstStatement
from .ast_expression_statement import ExpressionStatement as AstExpressionStatement
from .ast_constant import Constant as AstConstant
from .ast_declaration import Declaration as AstDeclaration
from .ast_function_call import FunctionCall as AstFunctionCall

class DependencyResolver:
    def __init__(self) -> None:
        pass

    def resolve(
        self,
        function_declaration: Declaration,
        resolve_primitives_immediately: bool = False
    ) -> Tuple[List[AstStatement], AstStatement]:
        arrange: List[AstStatement] = list()
        parameters: List[AstDeclaration] = list()
        used_names: Dict[str, int] = dict()
        function: SubroutineType = function_declaration.type

        parameter: Declaration
        for parameter in function.parameters:
            value: AstConstant = self.generate_primitive_constant(parameter.type)
            if not resolve_primitives_immediately:
                identifier: str = self.generate_identifier_for(parameter.identifier, used_names)

                arrange.append(AstDeclaration(parameter.type, identifier, value))
                parameters.append(AstConstant(identifier))
            else:
                parameters.append(value)

        act: AstStatement = None
        act_call = AstFunctionCall(function_declaration.identifier, parameters)
        if isinstance(function.return_type, PrimitiveType) and \
            function.return_type.name is not "void":
            act = AstDeclaration(function.return_type, "actual", act_call)
        else: act = AstExpressionStatement(act_call)

        return (arrange, act)

    def generate_identifier_for(self, formal_parameter: str, used_names: Dict[str, int] = list()) -> str:
        count: int = 0
        if formal_parameter in used_names:
            count = used_names[formal_parameter] + 1
        used_names[formal_parameter] = count
        return f'{formal_parameter}_{count}'

    def generate_primitive_constant(self, primitive: PrimitiveType, word_64bit: bool = True) -> AstConstant:
        if primitive.name == "char": return self.generate_integer(1, True)
        if primitive.name == "signed char": return self.generate_integer(1, True)
        if primitive.name == "unsigned char": return self.generate_integer(1, False)

        if primitive.name == "short": return self.generate_integer(2, True)
        if primitive.name == "short int": return self.generate_integer(2, True)
        if primitive.name == "signed short": return self.generate_integer(2, True)
        if primitive.name == "signed short int": return self.generate_integer(2, True)

        if primitive.name == "unsigned short": return self.generate_integer(2, False)
        if primitive.name == "unsigned short int": return self.generate_integer(2, False)


        if not word_64bit and primitive.name == "int": return self.generate_integer(2, True)
        if not word_64bit and primitive.name == "signed": return self.generate_integer(2, True)
        if not word_64bit and primitive.name == "signed int": return self.generate_integer(2, True)
        if word_64bit and primitive.name == "int": return self.generate_integer(4, True)
        if word_64bit and primitive.name == "signed": return self.generate_integer(4, True)
        if word_64bit and primitive.name == "signed int": return self.generate_integer(4, True)

        if not word_64bit and primitive.name == "unsigned": return self.generate_integer(2, False)
        if not word_64bit and primitive.name == "unsigned int": return self.generate_integer(2, False)
        if word_64bit and primitive.name == "unsigned": return self.generate_integer(4, False)
        if word_64bit and primitive.name == "unsigned int": return self.generate_integer(4, False)

        if primitive.name == "long": return self.generate_integer(4, True)
        if primitive.name == "long int": return self.generate_integer(4, True)
        if primitive.name == "signed long": return self.generate_integer(4, True)
        if primitive.name == "signed long int": return self.generate_integer(4, True)

        if primitive.name == "unsigned long": return self.generate_integer(4, False)
        if primitive.name == "unsigned long int": return self.generate_integer(4, False)

        if primitive.name == "long long": return self.generate_integer(8, True)
        if primitive.name == "long long int": return self.generate_integer(8, True)
        if primitive.name == "signed long long": return self.generate_integer(8, True)
        if primitive.name == "signed long long int": return self.generate_integer(8, True)

        if primitive.name == "unsigned long long": return self.generate_integer(8, False)
        if primitive.name == "unsigned long long int": return self.generate_integer(8, False)

        # on most systems, this is the IEEE 754 single-precision binary floating-point format (32 bits).
        if primitive.name == "float": return self.generate_decimal(4, True)
        # on most systems, this is the IEEE 754 double-precision binary floating-point format (64 bits)
        if primitive.name == "double": return self.generate_decimal(8, True)
        # 80 bits, but typically 96 bits or 128 bits in memory with padding bytes.
        if primitive.name == "long double": return self.generate_decimal(16, True)
        return None

    def generate_integer(self, bytes: int, signed: bool, suffix: str = "") -> AstConstant:
        def s_pow_2(byte_amount: int): return (2 ** (byte_amount * 2)) / 2
        def u_pow_2(byte_amount: int): return 2 ** (byte_amount * 2)
        ranges: Dict[(int, bool), Tuple[int, int]] = {
            # Ranges for signed values
            (1, True): (-s_pow_2(1), s_pow_2(1) - 1),
            (2, True): (-s_pow_2(2), s_pow_2(2) - 1),
            (4, True): (-s_pow_2(4), s_pow_2(4) - 1),
            (8, True): (-s_pow_2(8), s_pow_2(8) - 1),
            (16, True): (-s_pow_2(16), s_pow_2(16) - 1),
            # Ranges for unsigned values
            (1, False): (0, u_pow_2(1) - 1),
            (2, False): (0, u_pow_2(2) - 1),
            (4, False): (0, u_pow_2(4) - 1),
            (8, False): (0, u_pow_2(8) - 1),
            (16, False): (0, u_pow_2(16) - 1),
        }
        range: Tuple[int, int] = ranges[(bytes, signed)]
        value: int = random.randint(range[0], range[1])
        return AstConstant(f'{value}{suffix}')

    def generate_decimal(self, bytes: int, signed: bool, suffix: str = "") -> AstConstant:
        # TODO: Fix the generation of doubles which are plainly wrong
        value: int = random.uniform(-2 ** (bytes * 4), 2 ** (bytes * 4))
        if not signed: value = abs(value)
        return AstConstant(f'{value}{suffix}')