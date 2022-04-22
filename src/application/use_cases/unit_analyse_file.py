from typing import List
from utilities import FileHandler
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

class UnitAnalyseFileRequest(UseCaseRequest):
    def __init__(
        self,
        filepath: str,
        parser: Parser,
        unit: str,
    ) -> None:
        self._filepath = filepath
        self._parser = parser
        self._unit = unit
        super().__init__()

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def syntax(self) -> CSyntax:
        return self.language.syntax

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def language(self) -> Language:
        return self._parser.language

class UnitAnalyseFileResponse(UseCaseResponse):
    def __init__(self, tree: Tree, unit_function: Node) -> None:
        self._tree = tree
        self._unit_function = unit_function
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def unit_function(self) -> Node:
        return self._unit_function

    @property
    def found(self) -> bool:
        return self._unit_function is not None

class UnitAnalyseFileUseCase(
    UseCase[UnitAnalyseFileRequest, UnitAnalyseFileResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: UnitAnalyseFileRequest) -> UnitAnalyseFileResponse:
        # Step 1: Read the file and store its content
        file = open(request.filepath)
        contents: str = file.read()
        file.close()

        # Step 2: Parse the contents
        tree: Tree = request.parser.parse(contents)

        # Step 3: Retrieve all function definitions
        query: Query = request.language.query(
            request.syntax.function_declaration_query
        )
        capture: Capture = query.captures(tree.root)
        definitions: List[Node] = capture.nodes(
            request.syntax.get_function_definitions
        )

        # Step 4: Find the Function Under Test (FUT) - unit_function
        unit_function: Node = None
        for definition in definitions:
            identifier: Node = request.syntax.get_function_identifier(
                definition
            )
            if identifier is None: continue
            name: str = tree.contents_of(identifier)
            if name == request.unit:
                unit_function = definition
                break

        return UnitAnalyseFileResponse(
            tree,
            unit_function
        )