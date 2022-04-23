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

    @property
    def node(self) -> Node:
        return self._node

    @abstractmethod
    def apply(self) -> Tree:
        pass

    @abstractmethod
    def __str__(self) -> str:
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
        return self._parser.replace(
            self._tree,
            self._node,
            self._replacement
        )

    def __str__(self) -> str:
        return f"'{self._tree.contents_of(self._node)}' --> '{self._replacement}'"