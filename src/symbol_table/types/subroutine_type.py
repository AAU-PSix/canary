from typing import Generic, List
from . import Type
from ..declaration import TDeclaration

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