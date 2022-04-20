from inspect import trace
from unittest import TestCase
from . import CuTestResultsParser

class TestCuTestResultsParser(TestCase):
    def test_parse_summary_success(self):
        lines = [
            "..",
            "",
            "OK (2 tests)"
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 0)
        self.assertEqual(summary.success_count, 2)

    def test_parse_summary_success_with_a_trace(self):
        lines = [
            "Location=1",
            "..",
            "",
            "OK (2 tests)"
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        sequence = [ *test_results.trace.sequence ]

        self.assertEqual(len(sequence), 1)
        location_1 = sequence[0]
        self.assertIsNone(location_1.test)
        self.assertIsNone(location_1.unit)
        self.assertEqual(location_1.id, "1")

        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 0)
        self.assertEqual(summary.success_count, 2)

    def test_parse_summary_success_noisy_prefix(self):
        lines = [
            "  .....",
            "..",
            "",
            "OK (2 tests)"
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 0)
        self.assertEqual(summary.success_count, 2)

    def test_parse_summary_success_noisy_postfix(self):
        lines = [
            "..",
            "",
            "OK (2 tests)",
            "  .....",
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 0)
        self.assertEqual(summary.success_count, 2)

    def test_parse_summary_success_missing_end(self):
        lines = [
            "..",
            "",
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)

        self.assertIsNone(test_results)

    def test_parse_summary_failure(self):
        lines = [
            "FF",
            "",
            "There were 2 failures:",
            "1) addTest: /input/tests/AllTests.c:15: expected <1> but was <-1>",
            "2) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <-6>",
            "",
            "!!!FAILURES!!!",
            "Runs: 2 Passes: 0 Fails: 2",
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 2)
        self.assertEqual(summary.success_count, 0)

    def test_parse_summary_partial_success(self):
        lines = [
            ".F",
            "",
            "There was 1 failure:",
            "1) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <-6>",
            "",
            "!!!FAILURES!!!",
            "Runs: 2 Passes: 1 Fails: 1",
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 1)
        self.assertEqual(summary.success_count, 1)

    def test_parse_summary_no_test(self):
        lines = [
            "OK (0 tests)",
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary

        self.assertIsNotNone(test_results.trace)
        self.assertEqual(summary.test_count, 0)
        self.assertEqual(summary.failure_count, 0)
        self.assertEqual(summary.success_count, 0)

    def test_parse_complete_file(self):
        lines = [
            "Location=0",
            "Location=2",
            "Location=1",
            "Location=3",
            "Location=4",
            "Location=5",
            "Location=8",
            "Location=6",
            "Location=10",
            "Location=12",
            "Location=13",
            "Location=16",
            "Location=17",
            "Location=0",
            "Location=2",
            "Location=1",
            "Location=3",
            "Location=4",
            "Location=5",
            "Location=8",
            "Location=6",
            "Location=10",
            "Location=12",
            "Location=13",
            "Location=16",
            "Location=17",
            ".F",
            "",
            "There was 1 failure:",
            "1) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <-6>",
            "",
            "!!!FAILURES!!!",
            "Runs: 2 Passes: 1 Fails: 1",
        ]

        location_sequence = [
            0,
            2,
            1,
            3,
            4,
            5,
            8,
            6,
            10,
            12,
            13,
            16,
            17,
            0,
            2,
            1,
            3,
            4,
            5,
            8,
            6,
            10,
            12,
            13,
            16,
            17,
        ]

        parser = CuTestResultsParser()
        test_results = parser.parse(lines)
        summary = test_results.summary
        sequence = [ *test_results.trace.sequence ]

        for idx, location in enumerate(sequence):
            self.assertEqual(int(location.id), location_sequence[idx])

        traces = test_results.trace.split_on_location("0")
        self.assertEqual(len(traces), 2)

        self.assertEqual(len(traces[0]), 13)
        self.assertEqual(len(traces[1]), 13)

        self.assertEqual(summary.test_count, 2)
        self.assertEqual(summary.failure_count, 1)
        self.assertEqual(summary.success_count, 1)
