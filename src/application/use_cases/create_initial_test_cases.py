from utilities import FileHandler
from symbol_table import LexicalSymbolTable
from test_generator import (
    DependencyResolver,
    CuTestSuiteCodeGenerator,
    TestCase,
    TestSuite,
    CuTestLinker,
)
from ts import (
    Node,
)
from .use_case import *

class CreateInitialTestCasesRequest(UseCaseRequest):
    def __init__(
        self,
        symbols: LexicalSymbolTable,
        unit_identifier: str,
        test_filepath: str,
        linker_filepath: str,
    ) -> None:
        self._symbols = symbols
        self._unit_identifier = unit_identifier
        self._test_filepath = test_filepath
        self._linker_filepath = linker_filepath
        super().__init__()

    @property
    def symbols(self) -> LexicalSymbolTable:
        return self._symbols

    @property
    def unit_identifier(self) -> str:
        return self._unit_identifier

    @property
    def test_directory(self) -> str:
        return self._test_filepath

    @property
    def linker_filepath(self) -> str:
        return self._linker_filepath

class CreateInitialTestCasesResponse(UseCaseResponse): pass

class CreateInitialTestCasesUseCase(
    UseCase[CreateInitialTestCasesRequest, CreateInitialTestCasesResponse]
):
    def do(self, request: CreateInitialTestCasesRequest) -> CreateInitialTestCasesResponse:
        # Step 1: Create function declaration
        function = request.symbols.lookup(
            request.unit_identifier
        )

        # Step 2: Create test suite for the declaration
        resolver = DependencyResolver()
        arrange_act = resolver.resolve(function)
        test_case = TestCase(
            f'test_{function.identifier}',
            arrange_act[0],
            arrange_act[1],
            list()
        )
        test_suite = TestSuite(function.identifier, [ test_case ])

        # Step 3: Generate code for test suite
        code_generator = CuTestSuiteCodeGenerator()
        test_code = code_generator.visit_test_suite(test_suite)

        # Step 4: Write the test suite
        test_file: FileHandler = open(
            f'{request.test_directory}/{test_case.name}.h',
            "w+"
        )
        test_file.write('\n'.join(test_code))
        test_file.close()

        # Step 5: Connect the test suite with CanaryCuTest
        cutest_linker = CuTestLinker()
        linker_code = cutest_linker.link([ test_suite ])

        # Step 6: Write the new linker file
        linker_file = open(request.linker_filepath, "w+")
        linker_file.write('\n'.join(linker_code))
        linker_file.close()

        return CreateInitialTestCasesResponse()
