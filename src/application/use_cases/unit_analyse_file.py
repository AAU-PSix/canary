from typing import List, Tuple
from .parse_file import ParseFileRequest, ParseFileUseCase
from .unit_analyse_tree import UnitAnalyseTreeRequest, UnitAnalyseTreeUseCase
from ts import (
    Tree,
    Language,
    Node
)
from .use_case import *

class UnitAnalyseFileRequest(UseCaseRequest):
    def __init__(
        self,
        filepath: str,
        language: Language,
        unit: str = None,
    ) -> None:
        self._filepath = filepath
        self._language = language
        self._unit = unit
        super().__init__()

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def language(self) -> Language:
        return self._language

    @property
    def unit(self) -> str:
        return self._unit

class UnitAnalyseFileResponse(UseCaseResponse):
    def __init__(self, tree: Tree, unit_functions: List[Tuple[Node, str]]) -> None:
        self._tree = tree
        self._unit_functions = unit_functions
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def unit_functions(self) -> List[Tuple[Node, str]]:
        return self._unit_functions

    @property
    def found(self) -> bool:
        return len(self._unit_functions) > 0

class UnitAnalyseFileUseCase(
    UseCase[UnitAnalyseFileRequest, UnitAnalyseFileResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: UnitAnalyseFileRequest) -> UnitAnalyseFileResponse:
        # Step 1: Parse the file into the correct tree
        parse_file_request = ParseFileRequest(
            request.filepath, request.language
        )
        parse_file_response = ParseFileUseCase().do(
            parse_file_request
        )

        # Step 2: Analyse the parsed tree
        unit_analyse_tree_request = UnitAnalyseTreeRequest(
            parse_file_response.tree, request.language, request.unit
        )
        unit_analyse_tree_response = UnitAnalyseTreeUseCase().do(
            unit_analyse_tree_request
        )

        return UnitAnalyseFileResponse(
            parse_file_response.tree,
            unit_analyse_tree_response.unit_functions
        )