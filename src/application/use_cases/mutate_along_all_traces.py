from typing import List
from instrumentation_trace import Trace
from mutator import MutationStrategy
from cfa import LocalisedCFA
from ts import Tree
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
        strategy: MutationStrategy
    ) -> None:
        self._tree = tree
        self._traces = traces
        self._cfg = cfg
        self._strategy = strategy
        super().__init__()

    @property
    def tree(self) -> Trace:
        return self._tree

    @property
    def cfg(self) -> LocalisedCFA:
        return self._cfg

    @property
    def trace(self) -> List[Trace]:
        return self._traces

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

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
            print(trace_str)

            mutate_along_trace_request = MutateAlongTraceRequest(
                request.tree,
                trace,
                request.cfg,
                request.strategy
            )
            MutateAlongTraceUseCase().do(mutate_along_trace_request)
        return MutateAlongAllTracesResponse()
