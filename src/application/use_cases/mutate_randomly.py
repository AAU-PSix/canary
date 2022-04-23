from typing import List
from mutator import MutationStrategy
from test_results_parsing import ResultsParser
from ts import Tree, Parser, Node
from .run_mutation_test import RunMutationTestRequest, RunMutationTestResponse, RunMutationTestUseCase
from .run_test import RunTestRequest
from .parse_test_result import ParseTestResultRequest
from .use_case import UseCaseRequest, UseCaseResponse, UseCase

class MutateRandomlyRequest(UseCaseRequest):
    def __init__(
        self,
        node: Node,
        tree: Tree,
        parser: Parser,
        strategy: MutationStrategy,
        build_command: str,
        test_command: str,
        test_results_parser: ResultsParser,
        full_file_path: str,
        out: str = "",
        base: str = "",
    ) -> None:
        self._build_command = build_command
        self._test_command = test_command
        self._test_results_parser = test_results_parser
        self._parser = parser
        self._node = node
        self._tree = tree
        self._strategy = strategy
        self._full_file_path = full_file_path
        self._out = out
        self._base = base
        super().__init__()

    @property
    def build_command(self) -> str:
        return self._build_command

    @property
    def test_command(self) -> str:
        return self._test_command

    @property
    def test_results_parser(self) -> str:
        return self._test_results_parser

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def node(self) -> Node:
        return self._node

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

    @property
    def full_file_path(self) -> str:
        return self._full_file_path

    @property
    def out(self) -> str:
        return self._out

    @property
    def base(self) -> str:
        return self._base

class MutateRandomlyResponse(UseCaseResponse):
    def __init__(
        self,
        amount_killed: int,
        amount_survived: int,
        mutation_tests: List[RunMutationTestResponse],
    ) -> None:
        self._amount_killed = amount_killed
        self._amount_survived = amount_survived
        self._mutation_tests = mutation_tests
        super().__init__()

    @property
    def amount_killed(self) -> int:
        return self._amount_killed

    @property
    def amount_survived(self) -> int:
        return self._amount_survived

    @property
    def mutation_tests(self) -> List[RunMutationTestResponse]:
        return self._mutation_tests

class MutateRandomlyUseCase(
    UseCase[MutateRandomlyRequest, MutateRandomlyResponse]
):
    def do(self, request: MutateRandomlyRequest) -> MutateRandomlyResponse:
        amount_killed = 0
        amount_survived = 0
        mutation_tests: List[RunMutationTestResponse] = list()
        candidates = request.strategy.capture(
            request.node
        )
        for c_idx, candidate in enumerate(candidates):

            mutations = request.strategy.mutations(
                request.parser, request.tree, candidate
            )
            for m_idx, mutation in enumerate(mutations):
                test_results_path = f'{request.base}/{request.out}/mutant_{c_idx}_{m_idx}_test_results.txt'
                run_mutation_test_request = RunMutationTestRequest(
                    mutation,
                    request.full_file_path,
                    RunTestRequest(
                        request.build_command,
                        request.test_command,
                        test_results_path
                    ),
                    ParseTestResultRequest(
                        test_results_path,
                        request.test_results_parser
                    )
                )
                run_mutation_test_response = RunMutationTestUseCase().do(
                    run_mutation_test_request
                )
                mutation_tests.append(run_mutation_test_response)

                summary = run_mutation_test_response.test_results.summary
                if summary.failure_count > 0:
                    amount_killed += 1
                else: amount_survived += 1
        
        return MutateRandomlyResponse(
            amount_killed,
            amount_survived,
            mutation_tests
        )
