from ts import Node, Parser, Tree
from .tree_infection import TreeInfection

class TreeInfectionInsert(TreeInfection):
    def __init__(self, node: Node, nest: str) -> None:
        self._node = node
        self._nest = nest
        super().__init__(node.start_byte)

    def do(self, parser: Parser, tree: Tree) -> Tree:
        return parser.insert(tree, self._node, self._nest)