from typing import List
from instrumentation_trace import Trace
from mutator import MutationStrategy
from cfa import LocalisedCFA, LocalisedNode
from test_results_parsing import ResultsParser
from ts import Tree, Parser
from .use_case import *
from .mutate_randomly import MutateRandomlyRequest, MutateRandomlyUseCase

class MutateAlongAllTracesRequest(UseCaseRequest):
    def __init__(
        self,
        traces: List[Trace],
        localised_cfg: LocalisedCFA,
        tree: Tree,
        parser: Parser,
        strategy: MutationStrategy,
        build_command: str,
        test_command: str,
        test_results_parser: ResultsParser,
        full_file_path: str,
        out: str = "",
        base: str = ""
    ) -> None:
        self._traces = traces
        self._localised_cfg = localised_cfg
        self._build_command = build_command
        self._test_command = test_command
        self._test_results_parser = test_results_parser
        self._parser = parser
        self._tree = tree
        self._strategy = strategy
        self._full_file_path = full_file_path
        self._out = out
        self._base = base
        super().__init__()

    @property
    def traces(self) -> List[Trace]:
        return self._traces

    @property
    def localised_cfg(self) -> LocalisedCFA:
        return self._localised_cfg

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

class MutateAlongAllTracesResponse(UseCaseResponse):
    def __init__(self) -> None:
        self.amount_killed = 0
        self.amount_survived = 0
        super().__init__()

class MutateAlongAllTracesUseCase(
    UseCase[MutateAlongAllTracesRequest, MutateAlongAllTracesResponse]
):
    def do(self, request: MutateAlongAllTracesRequest) -> MutateAlongAllTracesResponse:
        # Step 1: Find all unique visited locations from all the traces
        visited_locations: List[str] = list()
        for trace in request.traces:
            for location in trace.sequence:
                if location.id not in visited_locations:
                    visited_locations.append(location.id)

        # Step 2: Find all the localised nodes we visited
        visited_nodes: List[LocalisedNode] = list()
        for location in visited_locations:
            for node in request.localised_cfg.nodes:
                if node.location == location:
                    visited_nodes.append(node)

        # Step 3: Randomly mutate on all nodes we visited
        response = MutateAlongAllTracesResponse()
        for visited_node in visited_nodes:
            mutate_randomly_request = MutateRandomlyRequest(
                visited_node.node,
                request.tree,
                request.parser,
                request.strategy,
                request.build_command,
                request.test_command,
                request.test_results_parser,
                request.full_file_path,
                request.out,
                request.base,
            )
            mutate_randomly_response = MutateRandomlyUseCase().do(
                mutate_randomly_request
            )
            response.amount_killed += mutate_randomly_response.amount_killed
            response.amount_survived += mutate_randomly_response.amount_survived
            visited_node.amount_killed = mutate_randomly_response.amount_killed
            visited_node.amount_survived = mutate_randomly_response.amount_survived

        # Step 4: Save the localised CFG
        request.localised_cfg.draw(
            request.tree, "localised_cfg_with_mutation_score"
        ).save(directory=f"{request.base}/{request.out}")

        print(f'{response.amount_killed} killed and {response.amount_survived} survived')
        return response