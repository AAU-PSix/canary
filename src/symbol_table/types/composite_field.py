from .type import Type

class CompositeField():
    """Structs and such with other types
    """
    def __init__(self, identifier: str, member: Type) -> None:
        self._identifier = identifier
        self._member = member

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def member(self) -> Type:
        return self._member