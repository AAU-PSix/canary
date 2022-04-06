from typing import List
from .c_type import CType
from .composite_type import CompositeType
from .composite_field import CompositeField

class CTypeStruct(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)