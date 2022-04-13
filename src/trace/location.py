from .test import Test
from .unit import Unit

class Location():
    def __init__(
        self,
        test: Test,
        unit: Unit,
        id: str
    ) -> None:
        self._test = test
        self._unit = unit
        self._id = id

    @property
    def test(self) -> Test:
        return self._test

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def id(self) -> str:
        return self._id