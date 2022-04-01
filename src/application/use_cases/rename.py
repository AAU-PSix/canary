import os
from .use_case import *

class RenameRequest(UseCaseRequest):
    def __init__(
        self,
        first_file_path: str,
        second_file_path: str,
    ) -> None:
        self._first_file_path = first_file_path
        self._second_file_path = second_file_path
        super().__init__()

    @property
    def file_path(self) -> str:
        return self._first_file_path

    @property
    def tmp_file_path(self) -> str:
        return self._second_file_path

class RenameResponse(UseCaseResponse): pass

class RenameUseCase(
    UseCase[RenameRequest, RenameResponse]
):  
    def do(self, request: RenameRequest) -> RenameResponse:
        os.rename(request._first_file_path, request._second_file_path)
        return RenameResponse()