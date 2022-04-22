from typing import List, Tuple
from instrumentation_trace import Trace
from mutator import MutationStrategy
from decorators import TweetHandler
from cfa import LocalisedCFA
from ts import Tree, Parser, Node
from cfa import LocalisedCFA
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

class MutateAlongTraceRequest(UseCaseRequest):
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
        trace: Trace,
        cfg: LocalisedCFA,
    ) -> None:
        self._parser = parser
        self._tree = tree
        self._trace = trace
        self._cfg = cfg
        self._strategy = strategy
        self._filepath = filepath
        self._results_parser = results_parser
        self._build_command = build_command
        self._test_command = test_command
        self._base = base
        self._out = out
        super().__init__()

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def cfg(self) -> LocalisedCFA:
        return self._cfg

    @property
    def trace(self) -> Trace:
        return self._trace

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

    @property
    def filepath(self) -> str:
        return self._filepath

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
    def base(self) -> str:
        return self._base

    @property
    def out(self) -> str:
        return self._out

class MutateAlongTraceResponse(UseCaseResponse): pass

class MutateAlongTraceUseCase(
    UseCase[MutateAlongTraceRequest, MutateAlongTraceResponse]
):
    def do(self, request: MutateAlongTraceRequest) -> MutateAlongTraceResponse:
        killed_mutants_count = 0
        survived_mutatans_count = 0

        # Step 1: Trace the execution to find the nodes
        tweet_handler = TweetHandler(
            request.tree
        )
        trace_nodes = list(
            filter(
                lambda x: not tweet_handler.is_location_tweet(x.node),
                [ *request.cfg.follow(None, request.trace) ]
            )
        )

        visited_trace_nodes: List[Tuple[str, Node]] = list()

        for t_idx, trace_node in enumerate(trace_nodes):
            curr_trace_node = (trace_node.location, trace_node.node)
            if curr_trace_node in visited_trace_nodes:
                continue
            visited_trace_nodes.append(curr_trace_node)

            candidates = request.strategy.capture(trace_node.node)
            for c_idx, candidate in enumerate(candidates):

                # Step 2: Get all possible mutations for the candidate
                mutations = request.strategy.mutations(
                    request.parser,
                    request.tree,
                    candidate
                )
                for m_idx, mutation in enumerate(mutations):
                    # Step 3: Write the mutated program
                    file = open(request.filepath, "w+")
                    mutated_tree = mutation.apply()
                    file.write(mutated_tree.text)
                    file.close()

                    # Step 4: Run tests
                    test_request = RunTestRequest(
                        request.build_command,
                        request.test_command,
                        f'{request.base}/{request.out}/mutant_{t_idx}_{c_idx}_{m_idx}_test_results.txt'
                    )
                    RunTestUseCase().do(test_request)

                    # Step 5: Parse test results
                    parse_test_results_request = ParseTestResultRequest(
                        test_request.out,
                        request.results_parser
                    )
                    parse_test_results_response = ParseTestResultUseCase().do(
                        parse_test_results_request
                    )
                    if parse_test_results_response.test_results.summary.failure_count > 0:
                        killed_mutants_count += 1
                    else:
                        survived_mutatans_count += 1

                    # Step 6: Revert to the instrumented program after mutation
                    file = open(request.filepath, "w+")
                    file.write(request.tree.text)
                    file.close()

        return MutateAlongTraceResponse()
