from unittest import TestCase

from .ffs_gnu_assert_results_parser import FfsGnuAssertResultsParser

class TestFfsGunAssertResultsParser(TestCase):
    def test_parse_without_assertion_and_only_locations(self):
        lines = [
            "",
            "Location=1",
            "",
            "Location=0",
            ""
        ]
        
        parser = FfsGnuAssertResultsParser()
        test_results = parser.parse(lines)

        sequence = [ *test_results.trace.sequence ]
        
        self.assertIsNone(test_results.summary.test_count)
        self.assertIsNone(test_results.summary.success_count)
        self.assertEqual(test_results.summary.failure_count, 0)
        
        self.assertEqual(len(sequence), 2)
        location_1 = sequence[0]
        self.assertIsNone(location_1.test)
        self.assertIsNone(location_1.unit)
        self.assertEqual(location_1.id, "1")
        location_0 = sequence[1]
        self.assertIsNone(location_0.test)
        self.assertIsNone(location_0.unit)
        self.assertEqual(location_0.id, "0")

    def test_parse_with_assertion_and_locations(self):
        lines = [
            "tests: tests/tests.c:154: test_core: Assertion `hydro_equal(a, b, sizeof a)' failed.",
            "",
            "Location=1",
            "",
            "Location=0",
            ""
        ]
        
        parser = FfsGnuAssertResultsParser()
        test_results = parser.parse(lines)

        sequence = [ *test_results.trace.sequence ]
        
        self.assertIsNone(test_results.summary.test_count)
        self.assertIsNone(test_results.summary.success_count)
        self.assertEqual(test_results.summary.failure_count, 1)
        
        self.assertEqual(len(sequence), 2)
        location_1 = sequence[0]
        self.assertIsNone(location_1.test)
        self.assertIsNone(location_1.unit)
        self.assertEqual(location_1.id, "1")
        location_0 = sequence[1]
        self.assertIsNone(location_0.test)
        self.assertIsNone(location_0.unit)
        self.assertEqual(location_0.id, "0")