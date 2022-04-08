from typing import List, Generic, TypeVar

TNode = TypeVar("TNode", bound="Node")

class Node(Generic[TNode]):
    def __init__(
        self,
        parent: TNode,
        children: List[TNode],
    ) -> None:
        self._parent = parent
        self._children = children

    @property
    def parent(self) -> TNode:
        return self._parent

    @property
    def siblings(self) -> List[TNode]:
        if self.parent is None: return [ ]
        return self.parent.children

    @property
    def sibling_count(self) -> int:
        return len(self.siblings)

    @property
    def next_sibling(self) -> TNode:
        if self.parent is None: return None
        index = self.siblings.index(self)
        # Check if the next siblings is out of bounds.
        if index + 1 == len(self.siblings): return None
        return self.siblings[index + 1]

    @property
    def previous_sibling(self) -> TNode:
        if self.parent is None: return None
        index = self.siblings.index(self)
        # Check if the next siblings is out of bounds.
        if index - 1 < 0: return None
        return self.siblings[index - 1]

    @property
    def has_previous_sibling(self) -> bool:
        return self.previous_sibling is not None

    @property
    def children(self) -> List[TNode]:
        return self._children

    @property
    def first_child(self) -> TNode:
        return self.children[0]

    @property
    def last_child(self) -> TNode:
        return self.children[-1]

    @property
    def child_count(self) -> int:
        return len(self.children)