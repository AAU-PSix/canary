from abc import ABC, abstractmethod
from ts import Tree, Node, Parser

class Mutation(ABC):
    def __init__(
        self,
        parser: Parser,
        tree: Tree,
        node: Node,
    ) -> None:
        self._parser = parser
        self._tree = tree
        self._node = node

    @abstractmethod
    def apply(self) -> Tree:
        pass

class ReplacementMutation(Mutation):
    def __init__(
        self,
        parser: Parser,
        tree: Tree,
        node: Node,
        replacement: str
    ) -> None:
        self._replacement = replacement
        super().__init__(parser, tree, node)

    def apply(self) -> Tree:
        self._parser.replace(
            self._tree,
            self._node,
            self._replacement
        )