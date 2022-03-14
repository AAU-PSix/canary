from typing import Optional, Iterable

from tree_sitter import TreeCursor as _TreeCursor
from .node import Node


class TreeCursor:
    def __init__(self, cursor: _TreeCursor) -> None:
        self._cursor = cursor

    @property
    def node(self) -> Node:
        return Node(self._cursor.node)

    def current_field_name(self) -> Optional[str]:
        return self._cursor.current_field_name()

    def goto_parent(self) -> bool:
        return self._cursor.goto_parent()

    def goto_first_child(self) -> bool:
        return self._cursor.goto_first_child()

    def goto_next_sibling(self) -> bool:
        return self._cursor.goto_next_sibling()

    def reset(self):
        while self.goto_parent(): pass

    def pre_order_traverse(self) -> Iterable[Node]:
        reached_root: bool = False
        while not reached_root:
            yield self.node
            if self.goto_first_child(): continue
            if self.goto_next_sibling(): continue

            retracng: bool = True
            while retracng:
                if not self.goto_parent():
                    retracng = False
                    reached_root = True
                if self.goto_next_sibling():
                    retracng = False