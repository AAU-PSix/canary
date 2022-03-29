from ts import LanguageLibrary
from .use_case import *

class InitializeSystemRequest(UseCaseRequest): pass
class InitializeSystemResponse(UseCaseResponse): pass

class InitializeSystemUseCase(
    UseCase[InitializeSystemRequest, InitializeSystemResponse]
):
    def do(self, _: InitializeSystemRequest) -> InitializeSystemResponse:
        LanguageLibrary.build()
        return InitializeSystemResponse()
