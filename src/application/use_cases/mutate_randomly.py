from mutator import MutationStrategy
from cfa import LocalisedCFA
from ts import Tree, Node, Parser
from .use_case import *
from .run_test import (
    RunTestRequest,
    RunTestUseCase
)
from .parse_test_result import (
    ParseTestResultRequest,
    ParseTestResultUseCase
)
from test_results_parsing import ResultsParser

class MutateRandomlyRequest(UseCaseRequest):
    def __init__(
        self,
        parser: Parser,
        tree: Tree,
        strategy: MutationStrategy,
        results_parser: ResultsParser,
        build_command: str,
        test_command: str,
        base: str,
        out: str,
        filepath: str,
        node: Node = None,
    ) -> None:
        self._parser = parser
        self._tree = tree
        self._node = node or tree.root
        self._strategy = strategy
        self._results_parser = results_parser
        self._build_command = build_command
        self._test_command = test_command
        self._base = base
        self._filepath = filepath
        self._out = out
        super().__init__()

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def node(self) -> LocalisedCFA:
        return self._node

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

    @property
    def results_parser(self) -> ResultsParser:
        return self._results_parser

    @property
    def build_command(self) -> str:
        return self._build_command

    @property
    def test_command(self) -> str:
        return self._test_command

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def base(self) -> str:
        return self._base

    @property
    def out(self) -> str:
        return self._out


class MutateRandomlyResponse(UseCaseResponse): pass

class MutateRandomlyUseCase(
    UseCase[MutateRandomlyRequest, MutateRandomlyResponse]
):
    def do(self, request: MutateRandomlyRequest) -> MutateRandomlyResponse:
        killed_mutants_count = 0
        survived_mutatans_count = 0

        # Step 1: Find all candidates
        candidates = request.strategy.capture(
            request.node
        )
        print("  Step 1: Find all candidates")

        # Step 2: Go through each candidate
        for c_idx, candidate in enumerate(candidates):
            print(f"    Found '{len(candidates)}' candidates and picked '{request.tree.contents_of(candidate)}' inside '{request.tree.contents_of(candidate.parent)}'")

            # Step 3: Get all mutations for the candidate
            mutations = request.strategy.mutations(
                request.parser, request.tree, candidate
            )
            print(f"    The candidate has {len(mutations)} possible mutations")
            
            for m_idx, mutation in enumerate(mutations):
                mutated_tree = mutation.apply()

                # Step 4: Write mutated program
                file = open(request.filepath, "w+")
                file.write(mutated_tree.text)
                file.close()
                print("  Step 4: Write mutated program")

                # Step 5: Run tests
                test_request = RunTestRequest(
                    request.build_command,
                    request.test_command,
                    f'{request.base}/{request.out}/mutant_{c_idx}_{m_idx}_test_results.txt'
                )
                RunTestUseCase().do(test_request)
                print("  Step 5: Run tests")

                # Step 6: Parse test results
                parse_test_results_request = ParseTestResultRequest(
                    test_request.test_stdout,
                    request.results_parser
                )
                parse_test_results_response = ParseTestResultUseCase().do(
                    parse_test_results_request
                )
                if parse_test_results_response.test_results.summary.failure_count > 0:
                    print("    Mutant was killed")
                    killed_mutants_count += 1
                else:
                    print("    Mutant survived")
                    survived_mutatans_count += 1

                print("  Step 6: Parse test results")

                # Step 7: Revert to the instrumented program after mutation
                file = open(request.filepath, "w+")
                file.write(request.tree.text)
                file.close()
                print("  Step 7: Revert to the instrumented program after mutation")

        print(f"**Stats** {killed_mutants_count} killed and {survived_mutatans_count} survived")

        return MutateRandomlyResponse()
