import re
from typing import List
from instrumentation_trace import (
    TraceParser,
    TraceTreeBuilder
)
from instrumentation_trace import Trace

class TestSummary():
    def __init__(
        self,
        test_count: int,
        failure_count: int,
        success_count: int
    ) -> None:
        self._test_count = test_count
        self._failure_count = failure_count
        self._success_count = success_count

    @property
    def test_count(self) -> int:
        return self._test_count

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def success_count(self) -> int:
        return self._success_count

class TestResults():
    def __init__(
        self,
        summary: TestSummary,
        trace: Trace = None
    ) -> None:
        self._summary = summary
        self._trace = trace

    @property
    def summary(self) -> TestSummary:
        return self._summary

    @property
    def trace(self) -> Trace:
        return self._trace

class CuTestResultsParser():
    def __init__(self) -> None:
        self._trace_parser = TraceParser(
            TraceTreeBuilder()
        )

    def parse(self, lines: List[str]) -> TestResults:
        for idx, line in enumerate(lines):
            if self._trace_parser.parse([ line ]):
                continue

            # Check if it is the beginning of the summary
            # Case 1: Only passes (First line is only "...")
            # Example:
            #   "..",
            #   "",
            #   "OK (2 tests)"
            if idx + 2 < len(lines) and \
                all("." == c for c in line) and \
                lines[idx + 1] == "" and \
                re.search("OK \([0-9]+ tests\)", lines[idx + 2]):
                # Since the line only consists of "." the
                #   length of it is the amount of successes.
                success_count = len(line)
                summary = TestSummary(
                    success_count, 0, success_count
                )
                return TestResults(
                    summary,
                    self._trace_parser.finish()
                )
            # Case 2: Has failures (First line is only "F")
            # Example:
            #   "FF"
            #   ""
            #   "There were 2 failures:"
            #   "1) addTest: /input/tests/AllTests.c:15: expected <1> but was <-1>"
            #   "2) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <-6>"
            #   ""
            #   "!!!FAILURES!!!"
            #   "Runs: 2 Passes: 0 Fails: 2"
            # Example:
            #   ".F"
            #   ""
            #   "There was 1 failure:"
            #   "1) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <-6>"
            #   ""
            #   "!!!FAILURES!!!"
            #   "Runs: 2 Passes: 1 Fails: 1"
            elif idx + 2 < len(lines) and \
                all("." == c or "F" == c for c in line) and \
                lines[idx + 1] == "" and \
                (re.search("There was 1 failure:", lines[idx + 2]) or \
                re.search("There were [0-9]+ failures:", lines[idx + 2])):
                sucess_count = line.count(".")
                failure_count = line.count("F")
                summary = TestSummary(
                    sucess_count + failure_count, failure_count, sucess_count
                )
                return TestResults(
                    summary,
                    self._trace_parser.finish()
                )
            # Case 3: No tests
            elif line == "OK (0 tests)":
                return TestResults(
                    TestSummary(0, 0, 0),
                    self._trace_parser.finish()
                )
