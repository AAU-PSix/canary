import random
from abc import ABC, abstractmethod
from typing import List
from ts import Tree, Node, NodeType, Parser
from .mutation import Mutation

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

    @abstractmethod
    def mutations(
        self,
        parser: Parser,
        tree: Tree,
        node: Node
    ) -> List[Mutation]:
        pass

    def choose(self, collection: list, rnd: float = None) -> any:
        if rnd is None: rnd = random.random()
        else: rnd = max(min(rnd, 1), 0)
        index: int = int(rnd * len(collection))
        return collection[index]

    def random_operator_range(
        self,
        range: List[List[NodeType]],
        rnd_range: float = None,
        rnd_operator: float = None
    ) -> NodeType:
        range: List[NodeType] = self.choose(range, rnd_range)
        return self.choose(range, rnd_operator)