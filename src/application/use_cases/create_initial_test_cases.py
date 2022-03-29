from .use_case import *

from utilities import FileHandler
from test_generator import (
    FunctionDeclaration,
    DependencyResolver,
    CuTestSuiteCodeGenerator,
    TestCase,
    TestSuite,
    CuTestLinker,
)
from ts import (
    Node,
    Tree,
)

class CreateInitialTestCasesRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        function: Node,
        test_filepath: str,
        linker_filepath: str,
    ) -> None:
        self._tree = tree
        self._function = function
        self._test_filepath = test_filepath
        self._linker_filepath = linker_filepath
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def function(self) -> Node:
        return self._function

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
        declaration = FunctionDeclaration.create_c(
            request.tree,
            request.function
        )

        # Step 2: Create test suite for the declaration
        resolver = DependencyResolver()
        arrange_act = resolver.resolve(declaration)
        test_case = TestCase(
            f'test_{declaration.name}',
            arrange_act[0],
            arrange_act[1],
            list()
        )
        test_suite = TestSuite(declaration.name, [ test_case ])

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
