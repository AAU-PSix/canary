from typing import Iterable, List
from graphviz import Digraph
from instrumentation_trace import Trace, Location
from ts import Tree
from .cfa import CFA
from .localised_node import LocalisedNode

class LocalisedCFA(CFA[LocalisedNode]):
    def __init__(self, root: LocalisedNode) -> None:
        super().__init__(root)

    def follow(self, unit_name: str, trace: Trace) -> Iterable[LocalisedNode]:
        if unit_name is not None:
            locations = [ location.id for location in trace.in_unit(unit_name) ]
        else:
            locations = [ location.id for location in trace.sequence ]

        current = self.root

        for idx, location in enumerate(locations):
            if idx + 1 < len(locations):
                next_location = locations[idx + 1]
            else: next_location = None

            # Step 1: Find the next location node
            if current.location != location:
                for outgoing in self.outgoing(current):
                    if outgoing.location == location:
                        current = outgoing

            # Step 2: Follow the current trace location
            for trace_node in self.follow_location(
                location,
                current,
                next_location
            ):
                current = trace_node
                yield trace_node

    def follow_location(self, location: str, start: LocalisedNode, next_location: str = None) -> Iterable[LocalisedNode]:
        if start.location != location:
            return

        found_end = False
        current = start
        while not found_end:
            yield current

            found_end = True
            for outgoing in self.outgoing(current):
                if next_location is not None and \
                    outgoing.location == next_location:
                    found_end = True
                    break

                elif outgoing.location == location:
                    current = outgoing
                    found_end = False
    
    def split_on_finals(self, trace: Trace) -> List["Trace"]:
        finals = [ node.location for node in self.finals ]
        
        traces: List["Trace"] = list()
        sequence: List[Location] = list()
        for curr in trace.sequence:
            sequence.append(curr)
            if curr.id in finals:
                if sequence is not None:
                    traces.append(Trace(sequence))
                sequence = list()
        traces.append(sequence)
        return traces

    def draw_along_paths(
        self,
        trace: Trace,
        tree: Tree,
        name: str,
        dot: Digraph = None
    ) -> Digraph:
        if dot is None: dot = Digraph(name)