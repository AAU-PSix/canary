from tree_sitter.binding import Query as _Query

from .capture import Capture
from .node import Node
from .file_point import FilePoint


class Query:
    def __init__(self, query: _Query) -> None:
        self._query = query

    def matches(self, node: Node):
        """Get a list of all the matches within the given node

        Args:
            node (Node): The root node to query from
        """
        self._query.macthes(node._node)

    def captures(
        self,
        node: Node,
        start_point: FilePoint = None,
        end_point: FilePoint = None,
    ) -> Capture:
        if start_point is None or end_point is None:
            native_capture = self._query.captures(node._node)
        else:
            native_capture = self._query.captures(node._node, start_point, end_point)
        return Capture.create_from_native_capture(native_capture)