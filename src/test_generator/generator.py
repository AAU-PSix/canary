from io import TextIOWrapper
from typing import List
from .ast import (
    Assertion,
    Declaration,
    Expression,
    Statement,
    TestCase,
    ASTVisitor,
    ExpressionStatement,
    Constant,
    Assignment,
    FunctionCall
)

class CuTestCodeGenerator(ASTVisitor):
    def __init__(self) -> None:
        self._lines: List[str] = list()

    def visit(self, test: TestCase) -> List[str]:
        self._write_line(f'void {test.name}(CuTest *ct)')
        self._write_line("{")
        self._write_line("// Arrange")
        for stmt in test.arrange: stmt.accept(self)
        self._write_line("// Act")
        if test.act is not None: test.act.accept(self)
        self._write_line("// Assert")
        for stmt in test.assertions: stmt.accept(self)
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
        self._write(f'{declaration._type} {declaration._identifier}')
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

    def _write(self, text: str) -> None:
        self._lines[-1] += text

    def _next_line(self) -> None:
        self._write_line("")

    def _write_line(self, line: str = "") -> None:
        self._lines.append(line)