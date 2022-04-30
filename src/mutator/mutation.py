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
    def apply(self, encoding: str = "utf8") -> Tree:
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

    def apply(self, encoding: str = "utf8") -> Tree:
        return self._parser.replace(
            self._tree,
            self._node,
            self._replacement,
            encoding
        )

    def __str__(self) -> str:
        return f"'{self._tree.contents_of(self._node)}' --> '{self._replacement}'"

class WrappedMutation(Mutation):
    def __init__(
        self,
        parser: Parser,
        tree: Tree,
        node: Node,
        prefix: str,
        postfix: str,
    ) -> None:
        self._prefix = prefix
        self._postfix = postfix
        super().__init__(parser, tree, node)
        self._replacement = f'{prefix}{self._tree.contents_of(self._node)}{postfix}'

    def apply(self, encoding: str = "utf8") -> Tree:
        return self._parser.replace(
            self._tree,
            self._node,
            self._replacement,
            encoding
        )

    def __str__(self) -> str:
        return f"'{self._tree.contents_of(self._node)}' --> '{self._replacement}'"
