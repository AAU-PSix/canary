from abc import ABC, abstractmethod
from typing import List
from .test_results import TestResults

class ResultsParser(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def parse(self, lines: List[str]) -> TestResults:
        pass