from typing import List
from .composite_field import CompositeField
from .type import Type

class CompositeType(Type):
    """Structured data like structs and their fields
    """
    def __init__(self, composition: List[CompositeField]) -> None:
        self._composition = composition
        super().__init__()

    @property
    def composition(self) -> List[CompositeField]:
        return self._composition
