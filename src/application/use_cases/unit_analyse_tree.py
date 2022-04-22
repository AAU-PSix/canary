from typing import List, Tuple
from ts import (
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
        unit: str = None,
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
    def __init__(self, unit_functions: List[Tuple[Node, str]]) -> None:
        self._unit_functions = unit_functions
        super().__init__()

    @property
    def unit_functions(self) -> List[Tuple[Node, str]]:
        return self._unit_functions

    @property
    def found(self) -> bool:
        return self._unit_functions is not None

class UnitAnalyseTreeUseCase(
    UseCase[UnitAnalyseTreeRequest, UnitAnalyseTreeResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: UnitAnalyseTreeRequest) -> UnitAnalyseTreeResponse:
        # Step 1: Get all the function definitions be query
        query: Query = request.language.query(
            request.syntax.function_declaration_query
        )
        capture: Capture = query.captures(request.tree.root)
        definitions: List[Node] = capture.nodes(
            request.syntax.get_function_definitions
        )

        # Step 2: Find all matching functions (If none then all of them)
        unit_functions: List[Node] = list()
        for definition in definitions:
            identifier: Node = request.syntax.get_function_identifier(definition)
            # This also works as a check for the definitions to be correct
            if identifier is None: continue
            name: str = request.tree.contents_of(identifier)

            if request.unit is None or \
                name == request.unit:
                unit_functions.append((definition, name))

        return UnitAnalyseTreeResponse(
            unit_functions
        )