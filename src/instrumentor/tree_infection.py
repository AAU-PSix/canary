from abc import ABC, abstractmethod
from ts import Parser, Tree

class TreeInfection(ABC):
    def __init__(self, last_byte_index: int) -> None:
        self._last_byte_index = last_byte_index
        super().__init__()

    @property
    def last_byte_index(self) -> int:
        return self._last_byte_index

    @abstractmethod
    def do(self, parser: Parser, tree: Tree) -> Tree: pass