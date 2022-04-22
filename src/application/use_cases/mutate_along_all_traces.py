from typing import List
from instrumentation_trace import Trace
from mutator import MutationStrategy
from cfa import LocalisedCFA
from ts import Tree, Parser
from .use_case import *
from .mutate_along_trace import (
    MutateAlongTraceRequest,
    MutateAlongTraceUseCase
)

class MutateAlongAllTracesRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        traces: List[Trace],
        cfg: LocalisedCFA,
        strategy: MutationStrategy,
        parser: Parser,
        results_parser: str,
        build_command: str,
        test_command: str,
        base: str,
        out: str,
        filepath: str,
    ) -> None:
        self._tree = tree
        self._traces = traces
        self._cfg = cfg
        self._strategy = strategy
        self._parser = parser
        self._results_parser = results_parser
        self._build_command = build_command
        self._test_command = test_command
        self._base = base
        self._out = out
        self._filepath = filepath
        super().__init__()

    @property
    def tree(self) -> Trace:
        return self._tree

    @property
    def cfg(self) -> LocalisedCFA:
        return self._cfg

    @property
    def traces(self) -> List[Trace]:
        return self._traces

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def results_parser(self) -> str:
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

    @property
    def filepath(self) -> str:
        return self._filepath

class MutateAlongAllTracesResponse(UseCaseResponse): pass

class MutateAlongAllTracesUseCase(
    UseCase[MutateAlongAllTracesRequest, MutateAlongAllTracesResponse]
):
    def do(self, request: MutateAlongAllTracesRequest) -> MutateAlongAllTracesResponse:
        visited_traces: List[str] = list()
        for trace in request._traces:
            trace_str = ""
            for location in trace.sequence:
                trace_str += f'{location.id} '

            if trace_str in visited_traces: continue
            visited_traces.append(trace_str)

            mutate_along_trace_request = MutateAlongTraceRequest(
                request.parser,
                request.tree,
                request.strategy,
                request.results_parser,
                request.build_command,
                request.test_command,
                request.base,
                request.out,
                request.filepath,
                trace,
                request.cfg,
            )
            MutateAlongTraceUseCase().do(mutate_along_trace_request)
        return MutateAlongAllTracesResponse()
