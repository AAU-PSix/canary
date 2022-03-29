from .use_case import *

from ts import LanguageLibrary

class InitializeSystemRequest(UseCaseRequest): pass
class InitializeSystemResponse(UseCaseResponse): pass

class InitializeSystemUseCase(
    UseCase[InitializeSystemRequest, InitializeSystemResponse]
):
    def do(self, _: InitializeSystemRequest) -> InitializeSystemResponse:
        LanguageLibrary.build()
        return InitializeSystemResponse()
