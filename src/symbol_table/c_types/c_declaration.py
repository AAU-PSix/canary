from typing import List
from ..lexical_declaration import LexicalDeclaration
from ..types.type import Type

class CDeclaration(LexicalDeclaration):
    def __init__(
        self,
        identifier: str,
        type: Type,
        lexical_index: int,
        storage_class_specifiers: List[str],
        type_qualifiers: List[str],
    ) -> None:
        self._storage_class_specifiers = storage_class_specifiers
        self._type_qualifiers = type_qualifiers
        super().__init__(identifier, type, lexical_index)

    @property
    def storage_class_specifiers(self) -> List[str]:
        return self._storage_class_specifiers

    @property
    def type_qualifiers(self) -> List[str]:
        return self._type_qualifiers