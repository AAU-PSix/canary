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

class CDeclaration(LexicalDeclaration):
    def __init__(
        self,
        identifier: str,
        type: "Type",
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


class Type(ABC):
    def __init__(self) -> None: pass

class PrimitiveType(Type):
    """int, double, and such
    """
    def __init__(self, name: str) -> None:
        self._name = name
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

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

class CompositeType(Type):
    """Structured data like structs and their fields
    """
    def __init__(self, composition: List[CompositeField]) -> None:
        self._composition = composition
        super().__init__()

    @property
    def composition(self) -> List[CompositeField]:
        return self._composition

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

class EnumType(Type):
    def __init__(self, enumerators: List[EnumField]) -> None:
        self._enumerators = enumerators
        super().__init__()

    @property
    def enumerators(self) -> List[EnumField]:
        return self._enumerators

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