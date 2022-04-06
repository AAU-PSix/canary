from typing import List
from .ast_statement import Statement
from .ast_assertion import Assertion

class TestCase:
    def __init__(
        self,
        name: str,
        arrange: List[Statement],
        act: Statement,
        assertions: List[Assertion]
    ) -> None:
        self._name = name
        self._arrange = arrange
        self._act = act
        self._assertions = assertions

    @property
    def name(self) -> str:
        return self._name

    @property
    def arrange(self) -> List[Statement]:
        return self._arrange

    @property
    def act(self) -> Statement:
        return self._act

    @property
    def assertions(self) -> List[Assertion]:
        return self._assertions
