from queue import Queue
from tree_sitter import TreeCursor as _TreeCursor
from .c_canary_factory import CCanaryFactory
from .c_tree_infestator import CTreeInfestator
from .tree_infection import TreeInfection
from ts import Tree, Node, Parser
from cfa import CFA

from tree_sitter import Tree as _Tree
from typing import Iterable, List
from ts.file_point import FilePoint
from ts.tree_cursor import TreeCursor


class LocalizedNode(Node):
    def __init__(self, location = -99) -> None:
        super().__init__()
        self.location = location
        
class LocalisedTreeCursor(TreeCursor):
    def __init__(self, cursor: _TreeCursor) -> None:
        super().__init__(cursor)

    
    def breadth_first_traverse(self, named_only: bool = False) -> Iterable[LocalizedNode]:
        # Since the tree is a DAG, then we dont
        # need tokeep track of the visited nodes.
        queue = Queue()
        queue.put(self.node)
        while (not queue.empty()):
            current: LocalizedNode = queue.get()
            if named_only and current.is_named: yield current
            elif not named_only: yield current
            for neighbour in current.children:
                if named_only and neighbour.is_named: queue.put(neighbour)





class LocalisedTreeInfection(TreeInfection):
    def __init__(self, last_byte_index: int, node:LocalizedNode) -> None:
        self.node: LocalizedNode = node
        super().__init__(last_byte_index)


class LocalisedCCanaryFactory(CCanaryFactory):
    def __init__(self) -> None:
        self.new_locations: List[LocalizedNode] = []
        super().__init__()

    def create_location_tweets(self, node: Node) -> Iterable[LocalisedTreeInfection]:
        node.location = self._current_location+1
        self.new_locations.append(node)
        tree_infections = super().create_location_tweets(node) # appends 1 to current location
        
        #Append decorated nodes to infection --- thus they become localized
        for tree_infection in tree_infections:
            tree_infection.node = node

        return tree_infections



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

    def walk(self) -> LocalisedTreeCursor:
        return super().walk()

    def line_traverse(self) -> Iterable[str]:
        return super().line_traverse()

class LocalisedCInfestator(CTreeInfestator):
    def __init__(self, parser: Parser, canary_factory: LocalisedCCanaryFactory) -> None:
        super().__init__(parser, canary_factory)

    def infect(self, tree: Tree, cfa: CFA) -> LocalisedTree:
        t = (super().infect(tree, cfa))
        return t

