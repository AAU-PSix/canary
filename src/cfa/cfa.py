from src.ts import Node
from typing import Dict, List

class CFANode:
    def __init__(self, node: Node) -> None:
        self.node = node

class CFAEdge:
    def __init__(self, source: CFANode, destination: CFANode) -> None:
        self.source = source
        self.destination = destination

class CFA:
    _root: CFANode
    _nodes: List[CFANode]
    _outgoing_edges: Dict[CFANode, List[CFAEdge]]
    _ingoing_edges: Dict[CFANode, List[CFAEdge]]

    def __init__(self, root: CFANode) -> None:
        self._root = root
        self._nodes = [ root ]
        self._outgoing_edges = dict()
        self._outgoing_edges[root] = list()
        self._ingoing_edges = dict()
        self._ingoing_edges[root] = list()

    def __contains__(self, node: CFANode) -> bool:
        return node in self._nodes

    @property
    def node_len(self) -> int:
        return len(self._nodes)

    @property
    def root(self) -> CFANode:
        return self._root

    def outgoing(self, source: CFANode) -> List[CFANode]:
        if source not in self._outgoing_edges:
            return list()
        children: List[CFANode] = list()
        for edge in self._outgoing_edges[source]:
            children.append(edge.destination)
        return children

    def ingoing(self, destination: CFANode) -> List[CFANode]:
        if destination not in self._ingoing_edges:
            return list()
        children: List[CFANode] = list()
        for edge in self._ingoing_edges[destination]:
            children.append(edge.source)
        return children

    def branch(self, source: CFANode, destination: CFANode) -> None:
        if source not in self._nodes:
            self._nodes.append(source)
            self._outgoing_edges[source] = list()
            self._ingoing_edges[source] = list()
        if destination not in self._nodes:
            self._nodes.append(destination)
            self._outgoing_edges[destination] = list()
            self._ingoing_edges[destination] = list()

        edge: CFAEdge = CFAEdge(source, destination)
        self._outgoing_edges[source].append(edge)
        self._ingoing_edges[destination].append(edge)

    def _remove_edge(self, edge: CFAEdge) -> None:
        # b -> a
        self._outgoing_edges[edge.source].remove(edge)
        self._ingoing_edges[edge.destination].remove(edge)

    def remove(self, source: CFANode) -> None:
        # b -> s -> a
        # b -> a
        for ingoing in self._ingoing_edges[source]:
            for outgoing in self._outgoing_edges[source]:
                self.branch(ingoing.source, outgoing.destination)

        for ingoing in self._ingoing_edges[source]:
            self._remove_edge(ingoing)
        for outgoing in self._outgoing_edges[source]:
            self._remove_edge(outgoing)
        self._nodes.remove(source)
        del self._ingoing_edges[source]
        del self._outgoing_edges[source]

    def replace(self, before: CFANode, after: CFANode) -> None:
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