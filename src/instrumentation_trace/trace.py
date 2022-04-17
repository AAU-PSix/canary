from typing import List, Iterable
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

    def __contains__(self, key: str) -> bool:
        return key in [ location.id for location in self.sequence ]

    def in_unit(self, unit: str) -> Iterable[Location]:
        result: List[Location] = list()
        for location in self.sequence:
            if location.unit.name == unit:
                result.append(location)
        return result

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