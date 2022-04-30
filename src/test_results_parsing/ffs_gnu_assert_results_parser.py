from abc import ABC, abstractmethod
from typing import List
from instrumentation_trace import (
    TraceParser,
    TraceTreeBuilder
)
from .test_summary import TestSummary
from .test_results import TestResults
from .resutls_parser import ResultsParser

class FfsGnuAssertResultsParser(ResultsParser):
    def __init__(self) -> None:
        pass

    def parse(self, lines: List[str]) -> TestResults:
        trace_parser = TraceParser(
            TraceTreeBuilder()
        )
        found_assertion = False
        for line in lines:
            if "Found: [" in line:
                found_assertion = True
            elif "Assertion" in line and \
                line.endswith("failed."):
                found_assertion = True
            elif trace_parser.parse([ line ]):
                continue
        return TestResults(
            TestSummary(
                None,
                1 if found_assertion else 0,
                None
            ),
            trace_parser.finish()
        )