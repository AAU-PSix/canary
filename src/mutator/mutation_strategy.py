from abc import ABC, abstractmethod
from typing import List
from ts import Tree, Node

class MutationStrategy(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def capture(self, node: Node) -> List[Node]:
        pass

    @abstractmethod
    def mutate(
        self,
        tree: Tree,
        node: Node,
        encoding: str = "utf8"
    ) -> Tree:
        pass
