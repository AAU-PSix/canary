from src.ts import Node, TreeCursor, Tree
from typing import Dict, List

class CFANode:
    def __init__(self, node: Node) -> None:
        self._node = node

    @property
    def node(self) -> Node:
        return self._node

class CFAEdge:
    def __init__(self, source: CFANode, destination: CFANode) -> None:
        self._source = source
        self._destination = destination

    @property
    def source(self) -> CFANode:
        return self._source

    @property
    def destination(self) -> CFANode:
        return self._destination

class CFA:
    _root: CFANode
    _nodes: List[CFANode]
    _outgoing_edges: Dict[CFANode, List[CFAEdge]]

    def __init__(self, root: CFANode) -> None:
        self._root = root
        self._nodes = [ root ]
        self._outgoing_edges = dict()
        self._outgoing_edges[root] = list()

    def __contains__(self, node: CFANode) -> bool:
        return node in self._nodes

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

    def branch(self, source: CFANode, destination: CFANode) -> None:
        if source not in self._nodes:
            self._nodes.append(source)
            self._outgoing_edges[source] = list()
        if destination not in self._nodes:
            self._nodes.append(destination)
            self._outgoing_edges[destination] = list()

        self._outgoing_edges[source].append(
            CFAEdge(source, destination)
        )