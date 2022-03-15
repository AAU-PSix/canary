from typing import Optional, Iterable
from queue import Queue

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

    def goto_next_named_sibling(self) -> bool:
        while self.goto_next_sibling():
            if self.node.is_named: return True
        return False

    def reset(self):
        while self.goto_parent(): pass

    def retrace_to(self, node: Node):
        while True:
            if self.node._node == node._node:
                break
            self.goto_parent()

    def pre_order_traverse(self, named_only: bool = False) -> Iterable[Node]:
        reached_root: bool = False
        while not reached_root:
            if named_only and self.node.is_named: yield self.node
            elif not named_only: yield self.node
            if self.goto_first_child(): continue
            if self.goto_next_sibling(): continue

            retracng: bool = True
            while retracng:
                if not self.goto_parent():
                    retracng = False
                    reached_root = True
                if self.goto_next_sibling():
                    retracng = False

    def breadth_first_traverse(self, named_only: bool = False) -> Iterable[Node]:
        # Since the tree is a DAG, then we dont
        # need tokeep track of the visited nodes.
        queue = Queue()
        queue.put(self.node)
        while (not queue.empty()):
            current: Node = queue.get()
            if named_only and current.is_named: yield current
            elif not named_only: yield current
            for neighbour in current.children:
                if named_only and neighbour.is_named: queue.put(neighbour)