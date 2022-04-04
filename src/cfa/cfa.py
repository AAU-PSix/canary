from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Iterable, TypeVar
from queue import Queue
from graphviz import Digraph
from ts import Tree, Node
from .cfa_edge import CFAEdge
from .cfa_node import CFANode

NodeType = TypeVar('NodeType', bound=CFANode)
EdgeType = TypeVar('EdgeType', bound=CFAEdge)

class CFAGeneric(Generic[NodeType, EdgeType], ABC):

    @abstractmethod
    def nodes(self) -> List[NodeType]:
        pass

    @abstractmethod
    def root(self) -> NodeType:
        pass

    @abstractmethod
    def finals(self) -> List[NodeType]:
        pass

    @abstractmethod
    def add_final(self, final: NodeType) -> bool:
        pass

    @abstractmethod
    def outgoing(self, source: NodeType) -> List[NodeType]:
        pass

    
    @abstractmethod
    def outgoing_edges(self, source: NodeType) -> List[CFAEdge]:
        pass

    @abstractmethod
    def ingoing(self, destination: NodeType) -> List[NodeType]:
        pass

    @abstractmethod
    def ingoing_edges(self, source: NodeType) -> List[CFAEdge]:
        pass
    
    @abstractmethod
    def branch(self, source: NodeType, destination: NodeType, label: str = None) -> None:
        pass

    @abstractmethod
    def _remove_edge(self, edge: CFAEdge) -> None:
        pass    

    @abstractmethod
    def remove(self, source: NodeType) -> None:
        pass

    @abstractmethod
    def replace(self, before: NodeType, after: NodeType) -> None:
        pass

    @abstractmethod
    def breadth_first_traverse(self) -> Iterable[NodeType]:
        pass


class CFA(CFAGeneric[CFANode, CFAEdge]):
    _root: CFANode
    _nodes: List[CFANode]
    _outgoing_edges: Dict[CFANode, List[CFAEdge]]
    _ingoing_edges: Dict[CFANode, List[CFAEdge]]
    _additional_finals: List[CFANode]

    def __init__(self, root: CFANode) -> None:
        self._root = root
        self._nodes = [ root ]
        self._outgoing_edges = dict()
        self._outgoing_edges[root] = list()
        self._ingoing_edges = dict()
        self._ingoing_edges[root] = list()
        self._additional_finals = list()

    def __contains__(self, node: CFANode) -> bool:
        return node in self._nodes

    @property
    def node_len(self) -> int:
        return len(self._nodes)

    @property
    def nodes(self) -> List[CFANode]:
        return self._nodes

    @property
    def root(self) -> CFANode:
        return self._root

    @property
    def finals(self) -> List[CFANode]:
        finals: List[CFANode] = list()
        for node in self._nodes:
            if len(self.outgoing_edges(node)) is 0:
                finals.append(node)
        return finals

    def add_final(self, final: CFANode) -> bool:
        if final not in self._nodes: return False
        self._additional_finals.append(final)
        return True

    def outgoing(self, source: CFANode) -> List[CFANode]:
        if source not in self._outgoing_edges:
            return list()
        children: List[CFANode] = list()
        for edge in self._outgoing_edges[source]:
            children.append(edge.destination)
        return children

    def outgoing_edges(self, source: CFANode) -> List[CFAEdge]:
        if source not in self._nodes:
            return list()
        return self._outgoing_edges[source]

    def ingoing(self, destination: CFANode) -> List[CFANode]:
        if destination not in self._nodes:
            return list()
        children: List[CFANode] = list()
        for edge in self._ingoing_edges[destination]:
            children.append(edge.source)
        return children

    def ingoing_edges(self, source: CFANode) -> List[CFAEdge]:
        return self._ingoing_edges[source]

    def branch(self, source: CFANode, destination: CFANode, label: str = None) -> None:
        if source not in self._nodes:
            self._nodes.append(source)
            self._outgoing_edges[source] = list()
            self._ingoing_edges[source] = list()
        if destination not in self._nodes:
            self._nodes.append(destination)
            self._outgoing_edges[destination] = list()
            self._ingoing_edges[destination] = list()

        edge: CFAEdge = CFAEdge(source, destination, label)
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
            if final is source: self._additional_finals.remove(final)

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

    def draw(self, tree: Tree, name: str, dot: Digraph = None) -> Digraph:
        if dot is None: dot = Digraph(name)

        def node_name(cfa_node: CFANode) -> str:
            if cfa_node is None: return f'None'
            node: Node = cfa_node.node
            if node is None: return f'None'
            location: int = cfa_node.node.end_byte
            sanitized_contents: str = tree.contents_of(node).replace(":", "")
            return f'l{location} {sanitized_contents} \n {node.type}, child of {node.parent.type}'

        dot.node("initial", shape="point")
        dot.edge("initial", node_name(self.root))

        finals: List[CFANode] = self.finals
        if len(finals) > 0:
            dot.node("final", shape="point")
            for final in self.finals:
                dot.edge(node_name(final), "final")

        for node in self._nodes:
            dot.node(node_name(node))
            for outgoing in self.outgoing_edges(node):
                dot.edge(
                    node_name(outgoing.source),
                    node_name(outgoing.destination),
                    outgoing.label
                )

        # dot.comment = tree.text
        dot.attr(label=tree.text.replace(":", "|"))
        return dot

    def breadth_first_traverse(self) -> Iterable[CFANode]:
        queue: Queue[CFANode] = Queue()
        visited: List[CFANode] = list()
        queue.put(self.root)
        visited.append(self.root)

        while not queue.empty():
            current: CFANode = queue.get()
            yield current
            for outgoing in self._outgoing_edges[current]:
                if outgoing.destination not in visited:
                    queue.put(outgoing.destination)
                    visited.append(outgoing.destination)