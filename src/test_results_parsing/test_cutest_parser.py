import unittest
from test_results_parsing.parser_cutest import CuTestParser, FailedCuTest
from typing import List

from . import *

class TestCutestParser(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_parse_string_with_colon(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["5) Test_CuAssertPtrEquals: /input/tests/AllTests.c:55: expected <Test Hest: Blæst> but was <Pøls: 1 2 3>"]

        expected_expected = "Test Hest: Blæst"
        expected_actual = "Pøls: 1 2 3"

        # Act
        failed_cutests = self._parser.parse(parsed_line)

        actual_expected = failed_cutests[0].expected
        actual_actual = failed_cutests[0].actual

        # Assert 
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)

    def test_parse_int_result(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["5) Test_CuAssertPtrEquals: /input/tests/AllTests.c:55: expected <100> but was <69>"]

        expected_expected = "100"
        expected_actual = "69"

        # Act
        failed_cutests = self._parser.parse(parsed_line)

        actual_expected = failed_cutests[0].expected
        actual_actual = failed_cutests[0].actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)
        
    def test_parse_double_result(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["5) Test_CuAssertPtrEquals: /input/tests/AllTests.c:55: expected <200.00> but was <69.00>"]

        expected_expected = "200.00"
        expected_actual = "69.00"

        # Act
        failed_cutests = self._parser.parse(parsed_line)
        
        actual_expected = failed_cutests[0].expected
        actual_actual = failed_cutests[0].actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)
    
    def test_parse_pointer_result(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["5) Test_CuAssertPtrEquals: /input/tests/AllTests.c:55: expected pointer <0x0x16c17e0> but was <0x0x16c1800>"]

        expected_expected = "0x0x16c17e0"
        expected_actual = "0x0x16c1800"

        # Act
        failed_cutests = self._parser.parse(parsed_line)

        actual_expected = failed_cutests[0].expected
        actual_actual = failed_cutests[0].actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)
    
    def test_parse_assert_result(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["5) Test_CuAssertGuguGaga: /input/tests/AllTests.c:55: assert failed"]

        expected_expected = "true"
        expected_actual = "false"

        # Act
        failed_cutests = self._parser.parse(parsed_line)

        actual_expected = failed_cutests[0].expected
        actual_actual = failed_cutests[0].actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)

    def test_parse_no_testname(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["/input/tests/AllTests.c:55: assert failed"]
        expected_fail_list:  List[FailedCuTest] = []

        # Act
        failed_cutests = self._parser.parse(parsed_line)
        
        # Assert
        self.assertEqual(failed_cutests, expected_fail_list)

    def test_parse_no_testmessage(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = ["500) Test_CuAssertHest: /input/tests/AllTests.c:55: Noget helt andet"]
        expected_fail_list:  List[FailedCuTest] = [None]

        # Act
        failed_cutests = self._parser.parse(parsed_line)
        
        # Assert
        self.assertEqual(failed_cutests, expected_fail_list)
    

    def test_single_parse_pointer(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = "5) Test_CuAssertPtrEquals: /input/tests/AllTests.c:55: expected pointer <0x0x16c17e0> but was <0x0x16c1800>"
        
        expected_expected = "0x0x16c17e0"
        expected_actual = "0x0x16c1800"

        # Act
        failed_cutest = self._parser.parse_single_line(parsed_line)

        actual_expected = failed_cutest.expected
        actual_actual = failed_cutest.actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)

    def test_single_single_parse_int(self) -> None:
        # Arrange
        self._parser = CuTestParser()
        parsed_line = "1) addTest_1_1: /input/tests/AllTests.c:25: expected <12> but was <1>"
        
        expected_expected = "12"
        expected_actual = "1"

        # Act
        failed_cutest = self._parser.parse_single_line(parsed_line)
        
        actual_expected = failed_cutest.expected
        actual_actual = failed_cutest.actual

        # Assert
        self.assertEqual(expected_expected, actual_expected)
        self.assertEqual(actual_actual, expected_actual)