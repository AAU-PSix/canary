from inspect import trace
from typing import List, Iterable

from decorators import (
    LocalisedCFA,
    LocalisedNode
)
from .location import Location

class Trace():
    def __init__(
        self,
        sequence: List[Location] = list()
    ) -> None:
        self._sequence = sequence

    @property
    def sequence(self) -> Iterable[Location]:
        return self._sequence

    def __len__(self) -> int:
        return len(self.sequence)

    def in_unit(self, unit: str) -> Iterable[Location]:
        result: List[Location] = list()
        for location in self.sequence:
            if location.unit.name == unit:
                result.append(location)
        return result

    def follow(self, unit_name: str, cfa: LocalisedCFA) -> Iterable[LocalisedNode]:
        if unit_name is not None:
            locations = [ location.id for location in self.in_unit(unit_name) ]
        else:
            locations = [ location.id for location in self.sequence ]

        current = cfa.root
        for location in locations:
            # Step 1: Find the next location node
            if current.location is not location:
                outgoins = cfa.outgoing(current)
                for outgoing in outgoins:
                    if outgoing.location is location:
                        current = outgoing
                        break

            # Step 2: Follow the current trace location
            for trace_node in self.follow_location(location, current, cfa):
                current = trace_node
                yield trace_node

    def follow_location(self, location: str, start: LocalisedNode, cfa: LocalisedCFA) -> Iterable[LocalisedNode]:
        if start.location is not location: return

        found_end = False
        current = start
        while not found_end:
            yield current

            found_end = True
            for outgoing in cfa.outgoing(current):
                if outgoing.location is location:
                    current = outgoing
                    found_end = False

    def split_on_location(self, location: str) -> List["Trace"]:
        traces: List["Trace"] = list()
        sequence: List[Location] = None
        for curr in self.sequence:
            if curr.id == location:
                if sequence is not None:
                    traces.append(Trace(sequence))
                sequence = list()
            sequence.append(curr)
        traces.append(sequence)
        return traces
    
    def split_on_finals(self, cfg: LocalisedCFA) -> List["Trace"]:
        finals = [ node.location for node in cfg.finals ]
        
        traces: List["Trace"] = list()
        sequence: List[Location] = list()
        for curr in self.sequence:
            sequence.append(curr)
            if curr.id in finals:
                if sequence is not None:
                    traces.append(Trace(sequence))
                sequence = list()
        traces.append(sequence)
        return traces