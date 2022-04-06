from typing import List
from .enum_field import EnumField
from .type import Type

class EnumType(Type):
    def __init__(self, enumerators: List[EnumField]) -> None:
        self._enumerators = enumerators
        super().__init__()

    @property
    def enumerators(self) -> List[EnumField]:
        return self._enumerators