from cfa import (
    CFA,
    CCFAFactory
)
from ts import (
    Tree,
    Node
)
from .use_case import *

class CreateCFGRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        root: Node = None,
    ) -> None:
        self._tree = tree
        self._root = root
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def root(self) -> Node:
        return self._root

class CreateCFGResponse(UseCaseResponse):
    def __init__(self, cfa: CFA) -> None:
        self._cfa = cfa
        super().__init__()

    @property
    def cfa(self) -> CFA:
        return self._cfa

class CreateCFGUseCase(
    UseCase[CreateCFGRequest, CreateCFGResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: CreateCFGRequest) -> CreateCFGResponse:
        cfg_factory = CCFAFactory(request.tree)
        cfg = cfg_factory.create(request.root)
        return CreateCFGResponse(cfg)