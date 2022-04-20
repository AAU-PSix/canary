from typing import Dict, Generic, List, Iterable, Tuple
from queue import Queue
from graphviz import Digraph

from .cfa_node import CFANode
from .cfa_edge import CFAEdge
from .t_cfa_node import TCFANode
from ts import Tree

class CFA(Generic[TCFANode]):
    _root: TCFANode
    _nodes: List[TCFANode]
    _outgoing_edges: Dict[TCFANode, List[CFAEdge[TCFANode]]]
    _ingoing_edges: Dict[TCFANode, List[CFAEdge[TCFANode]]]
    _additional_finals: List[Tuple[TCFANode, str]]

    def __init__(self, root: TCFANode) -> None:
        self._root = root
        self._nodes = [ root ]
        self._outgoing_edges = dict()
        self._outgoing_edges[root] = list()
        self._ingoing_edges = dict()
        self._ingoing_edges[root] = list()
        self._additional_finals = list()

    def __contains__(self, node: TCFANode) -> bool:
        return node in self._nodes

    @property
    def node_len(self) -> int:
        return len(self._nodes)

    @property
    def nodes(self) -> List[TCFANode]:
        return self._nodes

    @property
    def root(self) -> TCFANode:
        return self._root

    @property
    def finals(self) -> List[Tuple[TCFANode, str]]:
        finals: List[Tuple[TCFANode, str]] = list()
        for node_label in self._nodes:
            if len(self.outgoing_edges(node_label)) is 0:
                finals.append((node_label, None))
        for node_label in self._additional_finals:
            if node_label not in finals:
                finals.append(node_label)
        return finals

    def add_final(self, final: TCFANode, label: str = None) -> bool:
        if final not in self._nodes: return False
        self._additional_finals.append((final, label))
        return True

    def outgoing(self, source: TCFANode) -> List[TCFANode]:
        if source not in self._outgoing_edges:
            return list()
        children: List[TCFANode] = list()
        for edge in self._outgoing_edges[source]:
            children.append(edge.destination)
        return children

    def outgoing_edges(self, source: TCFANode) -> List[CFAEdge[TCFANode]]:
        if source not in self._nodes:
            return list()
        return self._outgoing_edges[source]

    def ingoing(self, destination: TCFANode) -> List[TCFANode]:
        if destination not in self._nodes:
            return list()
        children: List[TCFANode] = list()
        for edge in self._ingoing_edges[destination]:
            children.append(edge.source)
        return children

    def ingoing_edges(self, source: TCFANode) -> List[CFAEdge[TCFANode]]:
        return self._ingoing_edges[source]

    def branch(self, source: TCFANode, destination: TCFANode, label: str = None) -> None:
        if source not in self._nodes:
            self._nodes.append(source)
            self._outgoing_edges[source] = list()
            self._ingoing_edges[source] = list()
        if destination not in self._nodes:
            self._nodes.append(destination)
            self._outgoing_edges[destination] = list()
            self._ingoing_edges[destination] = list()

        edge: CFAEdge[TCFANode] = CFAEdge(source, destination, label)
        self._outgoing_edges[source].append(edge)
        self._ingoing_edges[destination].append(edge)

    def _remove_edge(self, edge: CFAEdge[TCFANode]) -> None:
        # b -> a
        self._outgoing_edges[edge.source].remove(edge)
        self._ingoing_edges[edge.destination].remove(edge)

    def remove(self, source: TCFANode) -> None:
        # b -> s -> a
        # b -> a
        for ingoing in self._ingoing_edges[source]:
            for outgoing in self._outgoing_edges[source]:
                self.branch(ingoing.source, outgoing.destination, ingoing.label)

        for node in self._ingoing_edges:
            for edge in self._ingoing_edges[node]:
                if edge.source is source or edge.destination is source:
                    self._remove_edge(edge)
        
        for node in self._outgoing_edges:
            for edge in self._outgoing_edges[node]:
                if edge.source is source or edge.destination is source:
                    self._remove_edge(edge)

        self._nodes.remove(source)
        del self._ingoing_edges[source]
        del self._outgoing_edges[source]

        for final in self._additional_finals:
            if final[0] is source: self._additional_finals.remove(final)

    def replace(self, before: TCFANode, after: TCFANode) -> None:
        for ingoing in self._ingoing_edges[before]:
            ingoing.destination = after
        for outgoing in self._outgoing_edges[before]:
            outgoing.source = after
        self._nodes.remove(before)
        self._nodes.append(after)
        self._ingoing_edges[after] = self._ingoing_edges[before]
        self._outgoing_edges[after] = self._outgoing_edges[before]
        del self._ingoing_edges[before]
        del self._outgoing_edges[before]

    def _cfa_node_name(self, tree: Tree, cfa_node: CFANode) -> str:
        if cfa_node is None: return f'CFA node is None'
        if cfa_node.node is None: return f'TS node is None'
        cfa_node_str = str(cfa_node)

        sanitized_contents: str = tree.contents_of(cfa_node.node).replace(":", "")
        return f'{cfa_node_str} {sanitized_contents} \n child of {cfa_node.node.parent.type}'

    def draw(self, tree: Tree, name: str, dot: Digraph = None) -> Digraph:
        if dot is None: dot = Digraph(name)

        dot.node("initial", shape="point")
        dot.edge("initial", self._cfa_node_name(tree, self.root))

        dot.node("final", shape="point")
        for final_label in self.finals:
            dot.edge(self._cfa_node_name(tree, final_label[0]), "final", final_label[1])

        for node in self._nodes:
            dot.node(self._cfa_node_name(tree, node))
            for outgoing in self.outgoing_edges(node):
                dot.edge(
                    self._cfa_node_name(tree, outgoing.source),
                    self._cfa_node_name(tree, outgoing.destination),
                    outgoing.label,
                )

        # dot.comment = tree.text
        dot.attr(label=tree.contents_of(self.root.node.parent).replace(":", "|"))
        return dot

    def breadth_first_traverse(self) -> Iterable[TCFANode]:
        queue: Queue[TCFANode] = Queue()
        visited: List[TCFANode] = list()
        queue.put(self.root)
        visited.append(self.root)

        while not queue.empty():
            current: TCFANode = queue.get()
            yield current
            for outgoing in self._outgoing_edges[current]:
                if outgoing.destination not in visited:
                    queue.put(outgoing.destination)
                    visited.append(outgoing.destination)

    def all_paths(self) -> List[List[TCFANode]]:
        visited: List[TCFANode] = list()
        paths: List[List[TCFANode]] = list()
        path: List[TCFANode] = list()

        frontier: List[TCFANode] = self.outgoing(self.root)
        visited.append(self.root)

        while len(frontier) > 0:
            # Step 1: Pop from the "stack"
            source: TCFANode = frontier.pop(-1)

            # Step 2: As long as the current "source" is not
            #   a destination from the current end of the path
            #   then backtrack until we reach it, this
            #   is then the new start of the path.
            while source not in self.outgoing(path[-1]):
                path.pop(-1)
            path.append(source)

            # Step 3: Add path if we are at a final
            if source in self.finals:
                paths.append(path)

            # Step 4: Add all un-visited neightbours to frontier
            for destination in self.outgoing(source):
                if destination not in visited:
                    frontier.append(destination)
                    visited.append(destination)

        return paths