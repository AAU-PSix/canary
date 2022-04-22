from .cutest_results_parser import CuTestResultsParser
from .ffs_gnu_assert_results_parser import FfsGnuAssertResultsParser
from .resutls_parser import ResultsParser

class ResultsParserFactory():
    def __init__(self) -> None:
        pass

    def create(self, name: str) -> ResultsParser:
        if name == "ffs_gnu_assert":
            return FfsGnuAssertResultsParser()
        if name == "cutest":
            return CuTestResultsParser()