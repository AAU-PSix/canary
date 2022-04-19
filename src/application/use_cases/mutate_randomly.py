from random import choice, random
from instrumentation_trace import Trace
from mutator import MutationStrategy
from cfa import LocalisedCFA
from ts import Tree, Node
from .use_case import *

class MutateRandomlyRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        strategy: MutationStrategy,
        node: Node = None,
    ) -> None:
        self._tree = tree
        self._node = node or tree.root
        self._strategy = strategy
        super().__init__()

    @property
    def tree(self) -> Trace:
        return self._tree

    @property
    def node(self) -> LocalisedCFA:
        return self._node

    @property
    def strategy(self) -> MutationStrategy:
        return self._strategy

class MutateRandomlyResponse(UseCaseResponse): pass

class MutateRandomlyUseCase(
    UseCase[MutateRandomlyRequest, MutateRandomlyResponse]
):
    def do(self, request: MutateRandomlyRequest) -> MutateRandomlyResponse:
        candidates = request.strategy.capture(
            request.node
        )
        candidate = choice(candidates)
        request.strategy.mutate(
            request.tree,
            candidate,
        )
        return MutateRandomlyResponse()
