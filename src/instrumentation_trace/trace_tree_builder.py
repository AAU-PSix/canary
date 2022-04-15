from typing import List
from .unit import Unit
from .location import Location
from .test import Test
from .trace import Trace

class TraceTreeBuilder():
    def __init__(self) -> None:
        self._unit_stack: List[Unit] = list()
        self._sequence: List[Location] = list()
        self._current_test = None

    @property
    def current_unit(self) -> Unit:
        if len(self._unit_stack) is 0:
            return None
        return self._unit_stack[-1]

    @property
    def current_test(self) -> Unit:
        return self._current_test

    @property
    def current_depth(self) -> int:
        return len(self._unit_stack)

    def start_test(self, test_name: str) -> "TraceTreeBuilder":
        self._sequence: List[Location] = list()
        self._current_test = Test(test_name)
        return self

    def start_unit(self, unit_name: str) -> "TraceTreeBuilder":
        self._unit_stack.append(
            Unit(unit_name)
        )
        return self

    def enter_location(
        self,
        location_name: str
    ) -> "TraceTreeBuilder":
        location = Location(
            self.current_test,
            self.current_unit,
            location_name
        )
        self._sequence.append(location)
        return self

    def end_unit(self) -> "TraceTreeBuilder":
        self._unit_stack.pop()
        return self

    def end_test(self) -> "TraceTreeBuilder":
        return self

    def build(self) -> Trace:
        return Trace(
            self._sequence
        )