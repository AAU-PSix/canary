from instrumentation_trace import Trace
from mutator import MutationStrategy
from decorators import TweetHandler
from cfa import LocalisedCFA
from ts import Tree
from .use_case import *

class MutateAlongTraceRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        trace: Trace,
        cfg: LocalisedCFA,
        strategy: MutationStrategy
    ) -> None:
        self._tree = tree
        self._trace = trace
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
    def trace(self) -> Trace:
        return self._trace

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

class MutateAlongTraceResponse(UseCaseResponse): pass

class MutateAlongTraceUseCase(
    UseCase[MutateAlongTraceRequest, MutateAlongTraceResponse]
):
    def do(self, request: MutateAlongTraceRequest) -> MutateAlongTraceResponse:
        tweet_handler = TweetHandler(
            request.tree
        )
        trace_nodes = list(
            filter(
                lambda x: not tweet_handler.is_location_tweet(x.node),
                [ *request.cfg.follow(None, request.trace) ]
            )
        )

        for trace_node in trace_nodes:
            candidates = request.strategy.capture(trace_node.node)
            
            for candidate in candidates:
                mutated_tree = request.strategy.mutate(
                    request.tree, candidate
                )
        return MutateAlongTraceResponse()
