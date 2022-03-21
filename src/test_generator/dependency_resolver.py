from typing import Dict, List, Tuple
from .ast import Constant, Declaration, Expression, ExpressionStatement, FunctionCall, FunctionDeclaration, Statement
import random

class DependencyResolver:
    def __init__(self) -> None:
        pass

    def resolve(
        self,
        function: FunctionDeclaration,
        resolve_primitives_immediately: bool = False
    ) -> Tuple[List[Statement], FunctionCall]:
        arrange: List[Statement] = list()
        parameters: List[Expression] = list()
        used_names: Dict[str, int] = dict()

        for parameter in function.formal_parameters:
            value: Constant = self.generate_primitive_constant(parameter.type)
            if not resolve_primitives_immediately:
                identifier: str = self.generate_identifier_for(parameter.identifier, used_names)
                declaration = Declaration(parameter.type, identifier, value)
                arrange.append(declaration)
                parameters.append(Constant(identifier))
            else:
                parameters.append(value)

        act: Statement = None
        act_call = FunctionCall(function.name, parameters)
        if function.return_type is not "void":
            act = Declaration(function.return_type, "actual", act_call)
        else: act = ExpressionStatement(act_call)

        return (arrange, act)

    def generate_identifier_for(self, formal_parameter: str, used_names: Dict[str, int] = list()) -> str:
        count: int = 0
        if formal_parameter in used_names:
            count = used_names[formal_parameter] + 1
        used_names[formal_parameter] = count
        return f'{formal_parameter}_{count}'

    def generate_primitive_constant(self, primitive: str, word_64bit: bool = True) -> Constant:
        if primitive == "char": return self.generate_integer(1, True)
        if primitive == "signed char": return self.generate_integer(1, True)
        if primitive == "unsigned char": return self.generate_integer(1, False)

        if primitive == "short": return self.generate_integer(2, True)
        if primitive == "short int": return self.generate_integer(2, True)
        if primitive == "signed short": return self.generate_integer(2, True)
        if primitive == "signed short int": return self.generate_integer(2, True)

        if primitive == "unsigned short": return self.generate_integer(2, False)
        if primitive == "unsigned short int": return self.generate_integer(2, False)


        if not word_64bit and primitive == "int": return self.generate_integer(2, True)
        if not word_64bit and primitive == "signed": return self.generate_integer(2, True)
        if not word_64bit and primitive == "signed int": return self.generate_integer(2, True)
        if word_64bit and primitive == "int": return self.generate_integer(4, True)
        if word_64bit and primitive == "signed": return self.generate_integer(4, True)
        if word_64bit and primitive == "signed int": return self.generate_integer(4, True)

        if not word_64bit and primitive == "unsigned": return self.generate_integer(2, False)
        if not word_64bit and primitive == "unsigned int": return self.generate_integer(2, False)
        if word_64bit and primitive == "unsigned": return self.generate_integer(4, False)
        if word_64bit and primitive == "unsigned int": return self.generate_integer(4, False)

        if primitive == "long": return self.generate_integer(4, True)
        if primitive == "long int": return self.generate_integer(4, True)
        if primitive == "signed long": return self.generate_integer(4, True)
        if primitive == "signed long int": return self.generate_integer(4, True)

        if primitive == "unsigned long": return self.generate_integer(4, False)
        if primitive == "unsigned long int": return self.generate_integer(4, False)

        if primitive == "long long": return self.generate_integer(8, True)
        if primitive == "long long int": return self.generate_integer(8, True)
        if primitive == "signed long long": return self.generate_integer(8, True)
        if primitive == "signed long long int": return self.generate_integer(8, True)

        if primitive == "unsigned long long": return self.generate_integer(8, False)
        if primitive == "unsigned long long int": return self.generate_integer(8, False)

        # on most systems, this is the IEEE 754 single-precision binary floating-point format (32 bits).
        if primitive == "float": return self.generate_decimal(4, True)
        # on most systems, this is the IEEE 754 double-precision binary floating-point format (64 bits)
        if primitive == "double": return self.generate_decimal(8, True)
        # 80 bits, but typically 96 bits or 128 bits in memory with padding bytes.
        if primitive == "long double": return self.generate_decimal(16, True)
        return None

    def generate_integer(self, bytes: int, signed: bool, suffix: str = "") -> Constant:
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
        return Constant(f'{value}{suffix}')

    def generate_decimal(self, bytes: int, signed: bool, suffix: str = "") -> Constant:
        # TODO: Fix the generation of doubles which are plainly wrong
        value: int = random.uniform(-2 ** (bytes * 4), 2 ** (bytes * 4))
        if not signed: value = abs(value)
        return Constant(f'{value}{suffix}')