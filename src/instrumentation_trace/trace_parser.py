from typing import Iterator
from .trace_tree_builder import TraceTreeBuilder
from .trace import Trace

class TraceParser():
    def __init__(self, builder = TraceTreeBuilder()) -> None:
        self._builder = builder

    @property
    def builder(self) -> TraceTreeBuilder:
        return self._builder

    def parse(self, lines: Iterator[str]) -> bool:
        for line in lines:
            split_line = line.split("=")
            action = split_line[0]

            information = split_line[1] if len(split_line) is 2 else None

            if action == "BeginTest":
                self.builder.start_test(information)
            elif action == "EndTest":
                self.builder.end_test()
            elif action == "BeginUnit":
                self.builder.start_unit(information)
            elif action == "EndUnit":
                self.builder.end_unit()
            elif action == "Location":
                self.builder.enter_location(information)
            else: break

    def finish(self) -> Trace:
        return self.builder.build()