from .c_type import CType
from symbol_table.types import Type

class CPointerType(CType):
    def __init__(self, multiple_indirection: int, type: Type) -> None:
        self._multiple_indirection = multiple_indirection
        self._type = type
        super().__init__()

    @property
    def type(self) -> Type:
        return self._type

    @property
    def multiple_indirection(self) -> int:
        return self._multiple_indirection