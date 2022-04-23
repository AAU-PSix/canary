from typing import Dict, List, Tuple
from instrumentation_trace import Trace
from mutator import MutationStrategy
from cfa import LocalisedCFA, LocalisedNode
from test_results_parsing import ResultsParser
from ts import Tree, Parser
from .use_case import *
from .mutate_randomly import MutateRandomlyRequest, MutateRandomlyResponse, MutateRandomlyUseCase

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
    def __init__(
        self,
        visited_locations: List[str],
        unvisited_locations: List[str],
        visited_nodes: List[LocalisedNode],
        unvisited_nodes: List[LocalisedNode],
        amount_killed: int,
        amount_survived: int,
        random_mutations_runs: List[Tuple[LocalisedNode, MutateRandomlyResponse]],
        unvisited_candidates: int,
        unvisited_mutations: int,
        visited_candidates: int,
        visited_mutations: int,
        amount_visited_locations: Dict[str, int],
        trace_count: int
    ) -> None:
        self._visited_locations = visited_locations
        self._unvisited_locations = unvisited_locations
        self._visited_nodes = visited_nodes
        self._unvisited_nodes = unvisited_nodes
        self._amount_killed = amount_killed
        self._amount_survived = amount_survived
        self._random_mutations_runs = random_mutations_runs
        self._unvisited_candidates = unvisited_candidates
        self._unvisited_mutations = unvisited_mutations
        self._visited_candidates = visited_candidates
        self._visited_mutations = visited_mutations
        self._amount_visited_locations = amount_visited_locations
        self._trace_count = trace_count
        super().__init__()

    @property
    def amount_visited_locations(self) -> Dict[str, int]:
        return self._amount_visited_locations

    @property
    def visited_locations(self) -> List[str]:
        return self._visited_locations

    @property
    def unvisited_locations(self) -> List[str]:
        return self._unvisited_locations

    @property
    def visited_nodes(self) -> List[LocalisedNode]:
        return self._visited_nodes

    @property
    def unvisited_nodes(self) -> List[LocalisedNode]:
        return self._unvisited_nodes

    @property
    def amount_killed(self) -> int:
        return self._amount_killed

    @property
    def amount_survived(self) -> int:
        return self._amount_survived

    @property
    def random_mutations_runs(self) -> List[Tuple[LocalisedNode, MutateRandomlyResponse]]:
        return self._random_mutations_runs

    @property
    def unvisited_candidates(self) -> int:
        return self._unvisited_candidates

    @property
    def unvisited_mutations(self) -> int:
        return self._unvisited_mutations

    @property
    def visited_candidates(self) -> int:
        return self._visited_candidates

    @property
    def visited_mutations(self) -> int:
        return self._visited_mutations

    @property
    def trace_count(self) -> int:
        return self._trace_count

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

        unvisited_locations: List[str] = list()
        
        for cfg_node in request.localised_cfg.nodes:
            if cfg_node.location not in visited_locations and \
                cfg_node.location not in unvisited_locations:
                    unvisited_locations.append(cfg_node.location)

        # Step 2: Find all the localised nodes we visited
        visited_nodes: List[LocalisedNode] = list()
        unvisited_nodes: List[LocalisedNode] = list()
        for cfa_node in request.localised_cfg.nodes:
            if cfa_node.location in visited_locations:
                visited_nodes.append(cfa_node)
            elif cfa_node.location in unvisited_locations:
                unvisited_nodes.append(cfa_node)

        # Step 3: For all un-/visited nodes how many mutations did we remove
        unvisited_candidates = 0
        unvisited_mutations = 0
        for cfa_node in unvisited_nodes:
            for candidate in request.strategy.capture(cfa_node.node):
                unvisited_candidates += 1
                unvisited_mutations += len(request.strategy.mutations(
                    request.parser,
                    request.tree,
                    candidate
                ))
        visited_candidates = 0
        visited_mutations = 0
        for cfa_node in visited_nodes:
            for candidate in request.strategy.capture(cfa_node.node):
                visited_candidates += 1
                visited_mutations += len(request.strategy.mutations(
                    request.parser,
                    request.tree,
                    candidate
                ))

        # Step 4: Randomly mutate on all nodes we visited
        amount_visited_locations: Dict[str, int] = dict()
        amount_killed = 0
        amount_survived = 0
        random_mutations_runs: List[MutateRandomlyResponse] = list()
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

            for mutation_test in mutate_randomly_response.mutation_tests:
                for location in mutation_test.test_results.trace.sequence:
                    if location.id not in amount_visited_locations:
                        amount_visited_locations[location.id] = 0
                    else: amount_visited_locations[location.id] += 1

            random_mutations_runs.append((visited_node, mutate_randomly_response))
            amount_killed += mutate_randomly_response.amount_killed
            amount_survived += mutate_randomly_response.amount_survived
            visited_node.amount_killed = mutate_randomly_response.amount_killed
            visited_node.amount_survived = mutate_randomly_response.amount_survived

        return MutateAlongAllTracesResponse(
            visited_locations,
            unvisited_locations,
            visited_nodes,
            unvisited_nodes,
            amount_killed,
            amount_survived,
            random_mutations_runs,
            unvisited_candidates,
            unvisited_mutations,
            visited_candidates,
            visited_mutations,
            amount_visited_locations,
            len(request.traces)
        )