from typing import List
from cfa import CFANode, CFAEdge
from cfa import LocalisedCFA

class ConversionStrategy:
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