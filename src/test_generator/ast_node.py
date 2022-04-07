from abc import ABC, abstractmethod
from typing import Any

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: Any): pass