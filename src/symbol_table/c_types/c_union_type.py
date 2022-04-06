from typing import List
from .c_type import CType
from symbol_table.types import (
    CompositeType,
    CompositeField
)

class CUnionType(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)