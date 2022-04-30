from abc import ABC
from random import choice
from typing import List
from .mutation_strategy import MutationStrategy
from ts import Tree, Node, Parser
from .mutation import Mutation

class CompositeStrategy(ABC):
    def __init__(self, composition: List[MutationStrategy]) -> None:
        self._composition = composition
        super().__init__()

    def capture(self, node: Node) -> List[Node]:
        result = list()
        for component in self._composition:
            result.extend(
                component.capture(node)
            )
        return result

    def mutate(
        self,
        tree: Tree,
        node: Node,
        encoding: str = "utf8"
    ) -> Tree:
        component = choice(self._composition)
        return component.mutate(tree, node, encoding)

    def mutations(
        self,
        parser: Parser,
        tree: Tree,
        node: Node
    ) -> List[Mutation]:
        result = list()
        for component in self._composition:
            result.extend(
                component.mutations(parser, tree, node)
            )
        return result