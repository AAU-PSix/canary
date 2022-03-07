from .node import Node
from tree_sitter.binding import Query as _Query

class Query:
    def __init__(self, query: _Query) -> None:
        self._query = query

    def matches(self, node: Node):
        """Get a list of all the matches within the given node

        Args:
            node (Node): The root node to query from
        """
        self._query(node._node)

    def captures(self, node: Node):
        # TODO: Not tested, since the parser isnt wrapped yet.
        return self._query.captures(node)