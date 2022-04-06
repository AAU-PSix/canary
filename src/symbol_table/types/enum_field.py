class EnumField():
    def __init__(self, identifier: str, value: int) -> None:
        self._identifier = identifier
        self._value = value

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def value(self) -> int:
        return self._value