from os import linesep, remove
from time import sleep
from test_results_parsing import (
    TestResults,
    CuTestResultsParser,
    ResultsParser
)
from .use_case import *

class ParseTestResultRequest(UseCaseRequest):
    def __init__(
        self,
        file_path: str,
        parser: ResultsParser,
    ) -> None:
        self._file_path = file_path
        self._parser = parser
        super().__init__()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def parser(self) -> ResultsParser:
        return self._parser

class ParseTestResultResponse(UseCaseResponse): 
    def __init__(
        self, 
        test_result: TestResults
    ) -> None:
        self._test_results = test_result
        super().__init__()
    
    @property
    def test_results(self) -> TestResults:
        return self._test_results

class ParseTestResultUseCase(
    UseCase[ParseTestResultRequest, ParseTestResultResponse]
):  
    def do(self, request: ParseTestResultRequest) -> ParseTestResultResponse:
        file = open(request.file_path, "r", errors="replace")
        contents: str = file.read()
        lines = contents.split(linesep)
        test_results = request.parser.parse(lines)

        remove(request.file_path)

        return ParseTestResultResponse(test_results)