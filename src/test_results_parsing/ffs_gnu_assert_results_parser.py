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
        self._trace_parser = TraceParser(
            TraceTreeBuilder()
        )

    def parse(self, lines: List[str]) -> TestResults:
        found_assertion = False
        for line in lines:
            if self._trace_parser.parse([ line ]):
                continue
            elif "Assertion" in line and \
                line.endswith("failed."):
                found_assertion = True
        return TestResults(
            TestSummary(
                None,
                1 if found_assertion else 0,
                None
            ),
            self._trace_parser.finish()
        )