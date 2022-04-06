from .declaration import Declaration
from .types.type import Type

class LexicalDeclaration(Declaration):
    def __init__(self, identifier: str, type: Type, lexical_index: int) -> None:
        self._lexical_index = lexical_index
        super().__init__(identifier, type)

    @property
    def lexical_index(self) -> int:
        return self._lexical_index