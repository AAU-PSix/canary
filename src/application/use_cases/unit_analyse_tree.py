from typing import List
from ts import (
    Parser,
    Tree,
    Query,
    Language,
    CSyntax,
    Capture,
    Node
)
from .use_case import *

class UnitAnalyseTreeRequest(UseCaseRequest):
    def __init__(
        self,
        tree: Tree,
        language: Language,
        unit: str,
    ) -> None:
        self._tree = tree
        self._language = language
        self._unit = unit
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def syntax(self) -> CSyntax:
        return self._language.syntax

    @property
    def language(self) -> Language:
        return self._language

class UnitAnalyseTreeResponse(UseCaseResponse):
    def __init__(self, unit_function: Node) -> None:
        self._unit_function = unit_function
        super().__init__()

    @property
    def unit_function(self) -> Node:
        return self._unit_function

    @property
    def found(self) -> bool:
        return self._unit_function is not None

class UnitAnalyseTreeUseCase(
    UseCase[UnitAnalyseTreeRequest, UnitAnalyseTreeResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: UnitAnalyseTreeRequest) -> UnitAnalyseTreeResponse:
        # Step 3: Retrieve all function definitions
        query: Query = request.language.query(
            request.syntax.function_declaration_query
        )
        capture: Capture = query.captures(request.tree.root)
        definitions: List[Node] = capture.nodes(
            request.syntax.get_function_definitions
        )

        # Step 4: Find the Function Under Test (FUT) - unit_function
        unit_function: Node = None
        for definition in definitions:
            identifier: Node = request.syntax.get_function_identifier(
                definition
            )
            name: str = request.tree.contents_of(identifier)
            if name == request.unit:
                unit_function = definition
                break

        return UnitAnalyseTreeResponse(
            unit_function
        )