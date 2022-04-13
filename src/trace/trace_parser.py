from typing import List
from .trace_tree_builder import TraceTreeBuilder
from .trace import Trace

class TraceParser():
    def parse(self, lines: List[str]) -> Trace:
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