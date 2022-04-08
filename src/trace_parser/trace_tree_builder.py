from typing import Iterable, List

class TraceParser():
    def parse(self, lines: List[str]) -> "Trace":
        builder = TraceTreeBuilder()
        for line in lines:
            split_line = line.split("=")
            action = split_line[0]
            
            information = split_line[1] if len(split_line) is 2 else None
            
            if action == "BeginTest":
                builder.start_test(information)
            elif action == "EndTest":
                builder.end_test()
            elif action == "BeginUnit":
                builder.start_unit(information)
            elif action == "EndUnit":
                builder.end_unit()
            elif action == "Location":
                builder.enter_location(information)

        return builder.build()

class TraceTreeBuilder():
    def __init__(self) -> None:
        self._unit_stack: List[Unit] = list()

    @property
    def current_unit(self) -> "Unit":
        if len(self._unit_stack) is 0:
            return None
        return self._unit_stack[-1]

    @property
    def current_test(self) -> "Unit":
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

    def build(self) -> "Trace":
        return Trace(
            self._sequence
        )

class Trace():
    def __init__(
        self,
        sequence: List["Location"] = list()
    ) -> None:
        self._sequence = sequence

    @property
    def sequence(self) -> Iterable["Location"]:
        return self._sequence

    def in_unit(self, unit: str) -> Iterable["Location"]:
        result: List[Location] = list()
        for location in self.sequence:
            if location.unit.name == unit:
                result.append(location)
        return result

class Test():
    def __init__(
        self,
        name: str
    ) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

class Unit():
    def __init__(
        self,
        name: str,
    ) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

class Location():
    def __init__(
        self,
        test: Test,
        unit: Unit,
        id: str
    ) -> None:
        self._test = test
        self._unit = unit
        self._id = id

    @property
    def test(self) -> Test:
        return self._test

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def id(self) -> str:
        return self._id