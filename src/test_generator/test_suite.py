from typing import List
from .test_case import TestCase

class TestSuite:
    def __init__(self, name: str, test_cases: List[TestCase]) -> None:
        self._name = name
        self._test_cases = test_cases

    @property
    def name(self) -> str:
        return self._name

    @property
    def test_cases(self) -> List[TestCase]:
        return self._test_cases