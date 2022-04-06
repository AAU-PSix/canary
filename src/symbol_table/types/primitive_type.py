from .type import Type

class PrimitiveType(Type):
    """int, double, and such
    """
    def __init__(self, name: str) -> None:
        self._name = name
        super().__init__()

    @property
    def name(self) -> str:
        return self._name