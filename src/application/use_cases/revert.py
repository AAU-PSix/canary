from .use_case import *

from utilities import (
    FileHandler
)

class RevertRequest(UseCaseRequest):
    def __init__(
        self,
        file_path: str,
        reversion : str,
    ) -> None:
        self._file_path = file_path
        self._reversion = reversion
        super().__init__()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def reversion(self) -> str:
        return self._reversion

class RevertResponse(UseCaseResponse): pass

class RevertUseCase(
    UseCase[RevertRequest, RevertResponse]
):  
    def do(self, request: RevertRequest) -> RevertResponse:
        new_inf_original_file: FileHandler = open(request.file_path, "w+")
        new_inf_original_file.write(request._reversion)
        new_inf_original_file.close()
        return RevertResponse()