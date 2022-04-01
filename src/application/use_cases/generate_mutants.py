from .use_case import *

from utilities import (
    FileHandler
)

from mutator import Mutator
from ts import (
    Parser,
    Tree,
)

class GenerateMutantsRequest(UseCaseRequest):
    def __init__(
        self,
        file_path: str,
        tmp_file_path: str,
    ) -> None:
        self._file_path = file_path
        self._tmp_file_path = tmp_file_path
        super().__init__()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def tmp_file_path(self) -> str:
        return self._tmp_file_path

class GenerateMutantsResponse(UseCaseResponse): pass

class GenerateMutantsUseCase(
    UseCase[GenerateMutantsRequest, GenerateMutantsResponse]
):  
    def do(self, request: GenerateMutantsRequest) -> GenerateMutantsResponse:
        # Step 6: Generate the mutant
        # Step 6.1: Read the original file, which is now the temp
        original_file: FileHandler = open(request._tmp_file_path, "r")
        original_contents: str = original_file.read()
        original_file.close()
        # Step 6.2: Parse the tree for the original program
        parser: Parser = Parser.c()
        tree: Tree = parser.parse(original_contents)
        # Step 6.3: Create the mutant
        mutator: Mutator = Mutator(parser)
        mutated_tree: Tree = mutator.mutate(tree)
        # Step 6.4: Write the mutant to the original filepath
        mutant_file: FileHandler = open(request._file_path, "w+")
        mutant_file.write(mutated_tree.text)
        mutant_file.close()

        return GenerateMutantsResponse()