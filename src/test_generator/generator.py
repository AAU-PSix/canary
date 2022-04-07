from typing import List
from abc import ABC

from .ast_visitor import ASTVisitor
from .ast_expression import Expression
from .ast_statement import Statement
from .ast_expression_statement import ExpressionStatement
from .ast_constant import Constant
from .ast_assignment import Assignment
from .ast_declaration import Declaration
from .ast_function_call import FunctionCall
from .ast_assertion import Assertion
from .test_suite import TestSuite
from .test_case import TestCase

class CodeGenerator(ABC):
    def __init__(self) -> None:
        self._lines: List[str] = list()
        self._indentation = 0
        super().__init__()

    def _write(self, text: str) -> None:
        self._lines[-1] += text

    def _indent(self) -> None:
        self._indentation += 1

    def _deindent(self) -> None:
        self._indentation -= 1

    def _next_line(self) -> None:
        self._write_line("")

    def _white_space_indentation(self, indentation: int = None) -> str:
        if indentation is None: indentation = self._indentation
        return indentation * "    "

    def _write_line(self, line: str = "") -> None:
        self._lines.append(f'{self._white_space_indentation()}{line}')

class CuTestSuiteCodeGenerator(CodeGenerator, ASTVisitor):
    def __init__(self) -> None:
        self._lines: List[str] = list()
        self._indentation = 0

    def visit_test_suite(self, suite: TestSuite) -> List[str]:
        self._lines = list()
        self._write_line(f'#ifndef TEST_{suite.name.upper()}')
        self._write_line(f'#define TEST_{suite.name.upper()}')
        self._write_line()
        self._write_line("#include <stdio.h>")
        self._write_line("#include <stdlib.h>")
        self._write_line()
        self._write_line('#include "CuTest.h"')
        self._write_line('#include "../src/original.h"')

        for test_case in suite.test_cases:
            self._write_line()
            self.visit_test_case(test_case)

        self._write_line()
        self._write_line(f'CuSuite *Create{suite.name}Suite()' + " {")
        self._indent()
        self._write_line("CuSuite *suite = CuSuiteNew();")
        for test_case in suite.test_cases:
            self._write_line(f'SUITE_ADD_TEST(suite, {test_case.name});')
        self._write_line("return suite;")
        self._deindent()
        self._write_line("}")

        self._write_line("#endif")

        return self._lines

    def visit_test_case(self, test: TestCase) -> List[str]:
        self._write_line(f'void {test.name}(CuTest *ct)' + ' {')
        self._indent()

        self._write_line("// Arrange")
        for stmt in test.arrange: stmt.accept(self)

        self._write_line("// Act")
        if test.act is not None:
            prev_indentation = self._indentation
            self._indentation = 0
            test.act.accept(self)
            self._lines[-1] = f'{self._white_space_indentation(prev_indentation)}CANARY_ACT({self._lines[-1]});'
            self._indentation = prev_indentation

        self._write_line("// Assert")
        for stmt in test.assertions: stmt.accept(self)

        self._deindent()
        self._write_line("}")
        return self._lines

    def visit_expression(self, expression: Expression): pass

    def visit_statement(self, statement: Statement): pass

    def visit_expression_statement(self, statement: ExpressionStatement):
        self._next_line()
        statement.epxression.accept(self)
        self._write(";")

    def visit_declaration(self, declaration: Declaration):
        self._write_line()
        self._write(f'{declaration.type.name} {declaration.identifier}')
        if declaration.initialization is not None:
            self._write(" = ")
            declaration.initialization.accept(self)
        self._write(";")

    def visit_assertion(self, assertion: Assertion):
        self._write_line()
        self._write("CuAssert(")
        assertion.expected.accept(self)
        self._write(", ")
        assertion.actual.accept(self)
        self._write(");")

    def visit_constant(self, constant: Constant):
        self._write(constant.value)

    def visit_assignment(self, assignment: Assignment):
        self._write_line(f'{assignment.lhs} = ')
        assignment.rhs.accept(self)
        self._write(";")

    def visit_function_call(self, function_call: FunctionCall):
        self._write(f'{function_call.name}(')
        for parameter in function_call.actual_parameters:
            parameter.accept(self)
            if parameter is not function_call.actual_parameters[-1]:
                self._write(", ")
        self._write(")")

class CuTestLinker(CodeGenerator):
    def link(self, suites: List[TestSuite]) -> List[str]:
        self._write_line("#ifndef CANARY_CUTEST")
        self._write_line("#define CANARY_CUTEST")
        self._write_line()
        self._write_line("#include \"CuTest.h\"")

        self._write_line()
        self._write_line("#include \"./test_add.h\"")
        self._write_line()
        self._write_line("CuSuite *CanarySuites() {")
        self._indent()
        self._write_line("CuSuite *suite = CuSuiteNew();")
        for suite in suites:
            self._write_line(f'CuSuiteAddSuite(suite, Create{suite.name}Suite());')
        self._write_line("return suite;")
        self._deindent()
        self._write_line("}")

        self._write_line("#endif")
        return self._lines