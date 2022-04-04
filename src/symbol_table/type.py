from typing import Generic, List, TypeVar
from abc import ABC


class Declaration():
    def __init__(self, identifier: str, type: "Type") -> None:
        self._identifier = identifier
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def type(self) -> "Type":
        return self._type

class LexicalDeclaration(Declaration):
    def __init__(self, identifier: str, type: "Type", lexical_index: int) -> None:
        self._lexical_index = lexical_index
        super().__init__(identifier, type)

    @property
    def lexical_index(self) -> int:
        return self._lexical_index

class Type(ABC):
    def __init__(self) -> None: pass

class CompositeField(Type):
    """Structs and such with other types
    """
    def __init__(self, identifier: str, members: Type) -> None:
        self._identifier = identifier
        self._member = members
        super().__init__()

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def member(self) -> Type:
        return self._member

class PrimitiveType(Type):
    """int, double, and such
    """
    def __init__(self, name: str) -> None:
        self._name = name
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

class CompositeType(Type):
    """Structured data like structs and their fields
    """
    def __init__(self, composition: List[CompositeField]) -> None:
        self._composition = composition
        super().__init__()

    @property
    def composition(self) -> List[CompositeField]:
        return self._composition

class AggregateType(Type):
    """Declaration of list/arrays
    """
    def __init__(self, type: Type) -> None:
        self._type = type
        super().__init__()

    @property
    def type(self) -> Type:
        return self._type

TDeclaration = TypeVar("TDeclaration", bound=Declaration)
class SubroutineType(Generic[TDeclaration], Type):
    """Referred to as a function, procedure, method, and subprogram,
        is code called and executed anywhere in a program
    """
    def __init__(
        self,
        return_type: Type = None,
        parameters: List[TDeclaration] = list()
    ) -> None:
        self._return_type = return_type
        self._parameters = parameters
        super().__init__()

    @property
    def has_return_type(self) -> bool:
        return self._return_type is not None

    @property
    def return_type(self) -> Type:
        return self._return_type

    @property
    def parameters(self) -> List[TDeclaration]:
        return self._parameters

    @property
    def arity(self) -> int:
        return len(self._parameters)