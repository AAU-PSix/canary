class FormalParameter:
    def __init__(self, identifier: str, type: str) -> None:
        self._identifier = identifier
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def type(self) -> str:
        return self._type