import unittest
from src.cutest_parser.parser_cutest import CuTestParser, FailedCuTest, FailedCuTestExpAss, FailedCuTestAss

from .. import *

class TestCutestParser(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_string_with_colon(self) -> None:
        self._parser = CuTestParser("/string_with_colon.results")
        self._parser.parse(self._parser.src)
        
        self.assertEqual()

