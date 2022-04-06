from .type import Type

class AggregateType(Type):
    """Declaration of list/arrays
    """
    def __init__(self, type: Type) -> None:
        self._type = type
        super().__init__()

    @property
    def type(self) -> Type:
        return self._type