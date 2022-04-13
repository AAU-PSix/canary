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

    def in_unit(self, unit: str) -> Iterable[Location]:
        result: List[Location] = list()
        for location in self.sequence:
            if location.unit.name == unit:
                result.append(location)
        return result