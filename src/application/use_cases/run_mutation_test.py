from mutator import Mutation
from test_results_parsing import TestResults
from ts import Node
from .use_case import UseCaseRequest, UseCaseResponse, UseCase
from .run_test import RunTestRequest, RunTestUseCase
from .parse_test_result import ParseTestResultRequest, ParseTestResultUseCase

class RunMutationTestRequest(UseCaseRequest):
    def __init__(
        self,
        mutation: Mutation,
        file_path: str,
        run_test_request: RunTestRequest,
        parse_test_results_request: ParseTestResultRequest,
    ) -> None:
        self._mutation = mutation
        self._file_path = file_path
        self._run_test_request = run_test_request
        self._parse_test_results_request = parse_test_results_request
        super().__init__()

    @property
    def mutation(self) -> Mutation:
        return self._mutation

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def run_test_request(self) -> RunTestRequest:
        return self._run_test_request

    @property
    def parse_test_results_request(self) -> ParseTestResultRequest:
        return self._parse_test_results_request

class RunMutationTestResponse(UseCaseResponse):
    def __init__(
        self,
        candidate: Node,
        mutation: Mutation,
        test_results: TestResults
    ) -> None:
        self._candidate = candidate
        self._test_results = test_results
        self._mutation = mutation
        super().__init__()

    @property
    def candidate(self) -> Node:
        return self._candidate

    @property
    def mutation(self) -> Mutation:
        return self._mutation

    @property
    def test_results(self) -> TestResults:
        return self._test_results

class RunMutationTestUseCase(
    UseCase[RunMutationTestRequest, RunMutationTestResponse]
):
    def do(self, request: RunMutationTestRequest) -> RunMutationTestResponse:
        # Step 1: Create the mutated tree
        mutated_tree = request.mutation.apply()

        # Step 2: Write the mutated tree to file
        file = open(request.file_path, "w+")
        file.write(mutated_tree.text)
        file.close()

        # Step 3: Run tests
        RunTestUseCase().do(
            request.run_test_request
        )

        # Step 4: Analyse the test results
        parse_test_results_response = ParseTestResultUseCase().do(
            request.parse_test_results_request
        )

        return RunMutationTestResponse(
            request.mutation.node,
            request.mutation,
            parse_test_results_response.test_results,
        )
