from typing import Generic
from .node import TNode

class Tree(Generic[TNode]):
    def __init__(self, root: TNode) -> None:
        self._root = root

    @property
    def root(self) -> TNode:
        return self._root