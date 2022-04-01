from typing import List, TypeVar
from abc import ABC

class Type(ABC):
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        return self._identifier

class CompositeField(Type):
    """Structs and such with other types
    """
    def __init__(self, identifier: str, members: List[Type]) -> None:
        self._members = members
        super().__init__(identifier)

    @property
    def members(self) -> List[Type]:
        return self._members

class PrimitiveType(Type):
    """int, double, and such
    """
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)

class CompositeType(Type):
    """Structured data like structs and their fields
    """
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        self._composition = composition
        super().__init__(identifier)

    @property
    def composition(self) -> List[CompositeField]:
        return self._composition

class AggregateType(Type):
    """Declaration of list/arrays
    """
    def __init__(self, type: Type) -> None:
        super().__init__(type)

class SubroutineType(Type):
    """Referred to as a function, procedure, method, and subprogram,
        is code called and executed anywhere in a program
    """
    def __init__(
        self,
        identifier: str,
        return_type: Type = None,
        parameters: List[Type] = list()
    ) -> None:
        self._return_type = return_type
        self._parameters = parameters
        super().__init__(identifier)

    @property
    def has_return_type(self) -> bool:
        return self._return_type is not None

    @property
    def return_type(self) -> Type:
        return self._return_type

    @property
    def parameters(self) -> List[Type]:
        return self._parameters
