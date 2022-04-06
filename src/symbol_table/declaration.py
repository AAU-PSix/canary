from typing import TypeVar
from .types.type import Type

TDeclaration = TypeVar("TDeclaration", bound="Declaration")

class Declaration():
    def __init__(self, identifier: str, type: Type) -> None:
        self._identifier = identifier
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def type(self) -> Type:
        return self._type