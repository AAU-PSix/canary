from abc import ABC, abstractmethod
from typing import TypeVar, Generic

class UseCaseRequest(ABC): pass
class UseCaseResponse(ABC): pass

TRequest = TypeVar("TRequest", bound=UseCaseRequest)
TResponse = TypeVar("TResponse", bound=UseCaseRequest)
class UseCase(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    def do(self, request: TRequest) -> TResponse:
        pass