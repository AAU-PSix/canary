from .c_canary_factory import CCanaryFactory
from .c_tree_infestator import CTreeInfestator
from .tree_infection import TreeInfection
from ts import Tree, Node, Parser
from cfa import CFA

from tree_sitter import Tree as _Tree
from typing import Iterable, List
from ts.file_point import FilePoint
from ts.tree_cursor import TreeCursor


class LocalisedTreeInfection(TreeInfection):
    def __init__(self, last_byte_index: int, location:int) -> None:
        self.location = location
        super().__init__(last_byte_index)



class LocalizationDecoratorCFactory(CCanaryFactory):
    def __init__(self) -> None:
        self.node_locations: dict[Node, int]
        super().__init__()

    def create_location_tweets(self, node: Node) -> Iterable[LocalisedTreeInfection]:
        self.node_locations[node] = self._current_location+1
        tree_infections = super().create_location_tweets(node)
        for tree_infection in tree_infections:
            tree_infection.location = self._current_location

        return tree_infections


class LocalizedNode(Node):
    def __init__(self) -> None:
        super().__init__()

class LocalisedTree(Tree):
    def __init__(self, tree: _Tree) -> None:
        super().__init__(tree)

    @property
    def root_node(self) -> LocalizedNode:
        return super().root_node

    @property
    def text(self) -> str:
        return super().text

    @property
    def lines(self) -> List[str]:
        return super().lines

    def edit(self, start_byte: int, old_end_byte: int, new_end_byte: int, start_point: FilePoint, old_end_point: FilePoint, new_end_point: FilePoint) -> None:
        return super().edit(start_byte, old_end_byte, new_end_byte, start_point, old_end_point, new_end_point)

    def contents_of(self, node: LocalizedNode) -> str:
        return super().contents_of(node)

    def walk(self) -> TreeCursor:
        return super().walk()

    def line_traverse(self) -> Iterable[str]:
        return super().line_traverse()



class LocalisationInfestator(CTreeInfestator):
    def __init__(self, parser: Parser, canary_factory: LocalizationDecoratorCFactory) -> None:
        super().__init__(parser, canary_factory)

    def infect(self, tree: Tree, cfa: CFA) -> Tree:
        t =  super().infect(tree, cfa)