from symbol_table import (
    CSymbolTable,
    CSymbolTableFiller,
    Tree
)
from ts import (
    CSyntax,
    Tree as TsTree,
    Language,
)
from .use_case import *

class CreateSymbolTableRequest(UseCaseRequest):
    def __init__(
        self,
        tree: TsTree,
        syntax: CSyntax
    ) -> None:
        self._tree = tree
        self._syntax = syntax
        super().__init__()

    @property
    def tree(self) -> TsTree:
        return self._tree

    @property
    def syntax(self) -> Language:
        return self._syntax

class CreateSymbolTableResponse(UseCaseResponse):
    def __init__(self, tree: Tree[CSymbolTable]) -> None:
        self._tree = tree
        super().__init__()

    @property
    def tree(self) -> Tree[CSymbolTable]:
        return self._tree

class CreateSymbolTableUseCase(
    UseCase[CreateSymbolTableRequest, CreateSymbolTableResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: CreateSymbolTableRequest) -> CreateSymbolTableResponse:
        # Step 1: Create symbol table filler
        filler = CSymbolTableFiller(
            request.syntax
        )

        # Step 2: Fill tables
        root = filler.fill(
            request.tree
        )

        return CreateSymbolTableResponse(
            root
        )