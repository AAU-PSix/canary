from typing import List, Tuple, Callable

from .node import Node


class Capture:
    def __init__(self, capture: List[Tuple[Node, str]]) -> None:
        self._capture = capture

    def __iter__(self) -> any:
        return self._capture.__iter__()

    def __next__(self) -> Tuple[Node, str]:
        return self._capture.__next__()

    def __getitem__(self, idx: int) -> Tuple[Node, str]:
        return self._capture[idx]

    def __len__(self) -> int:
        return len(self._capture)

    def first(self) -> Tuple[Node, str]:
        return self._capture[0]

    def last(self) -> Tuple[Node, str]:
        return self._capture[-1]

    def nodes(self, func: Callable[[Node], Node] = lambda node: node) -> List[Node]:
        nodes: List[Node] = list()
        for result in self:
            nodes.append(func(result[0]))
        return nodes

    @staticmethod
    def create_from_native_capture(capture: Tuple[any, str]) -> "Capture":
        result: List[Tuple[Node, str]] = list()
        for c in capture:
            # noinspection PyTypeChecker
            capture_node: Node = Node(c[0])
            capture_field: str = c[1]
            capture_tuple: Tuple[Node, str] = (capture_node, capture_field)
            result.append(capture_tuple)
        return Capture(result)