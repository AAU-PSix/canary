from utilities import FileHandler
from ts import (
    Parser,
    Tree,
    Language,
)
from .use_case import *

class ParseFileRequest(UseCaseRequest):
    def __init__(
        self,
        filepath: str,
        language: Language,
    ) -> None:
        self._filepath = filepath
        self._language = language
        super().__init__()

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def language(self) -> Language:
        return self._language

    @property
    def parser(self) -> Parser:
        return Parser.create_with_language(
            self._language
        )

class ParseFileResponse(UseCaseResponse):
    def __init__(self, tree: Tree) -> None:
        self._tree = tree
        super().__init__()

    @property
    def tree(self) -> Tree:
        return self._tree

class ParseFileUseCase(
    UseCase[ParseFileRequest, ParseFileResponse]
):
    def __init__(self) -> None:
        super().__init__()

    def do(self, request: ParseFileRequest) -> ParseFileResponse:
        # Step 1: Read the file and store its content
        file: FileHandler = open(request.filepath)
        contents: str = file.read()
        file.close()

        # Step 2: Parse the contents
        tree: Tree = request.parser.parse(contents)

        return ParseFileResponse(tree)