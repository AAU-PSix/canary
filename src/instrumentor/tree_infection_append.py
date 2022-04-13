from ts import Node, Parser, Tree
from .tree_infection import TreeInfection

class TreeInfectionAppend(TreeInfection):
    def __init__(self, node: Node, nest: str) -> None:
        self._node = node
        self._nest = nest
        # We add the length of the nest because the sum
        #   should be th eindex of the furthest (greates)
        #   affected byte of the source in order to be
        #   able to sort the TreeInfection(s) correctly.
        super().__init__(node.end_byte)

    def do(self, parser: Parser, tree: Tree) -> Tree:
        return parser.append(tree, self._node, self._nest)