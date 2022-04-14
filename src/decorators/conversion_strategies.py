from abc import ABC, abstractmethod
from typing import List
from cfa import CFANode, CFA, CFAEdge
from . import LocalisedCFA

class EdgeConversionStrategy(ABC):
    @abstractmethod
    def convert_edges(
        self,
        edges: List[CFAEdge],
        converted_edges:List[CFAEdge],
        localised_cfa: CFA,
        converted_nodes: List[CFANode]
    ):
        pass


class CFANodeToLocationConversionStrategy(EdgeConversionStrategy):
    def convert_edges(
        self,
        edges: List[CFAEdge],
        converted_edges: List[CFAEdge],
        localised_cfa: LocalisedCFA,
        converted_nodes: List[CFANode]
    ):
        for edge in edges:
            if edge in converted_edges: continue
            localised_cfa.branch(
                converted_nodes[edge.source],
                converted_nodes[edge.destination],
                edge.label
            )
            converted_edges.append(edge)