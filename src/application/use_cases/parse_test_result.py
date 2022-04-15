from os import linesep
from typing import List
from test_results_parsing import (
    TestResults,
    CuTestResultsParser
)
from .use_case import *

class ParseTestResultRequest(UseCaseRequest):
    def __init__(
        self,
        file_path: str
    ) -> None:
        self._file_path = file_path
        super().__init__()

    @property
    def file_path(self) -> str:
        return self._file_path


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
        parser = CuTestResultsParser()
        file = open(request.file_path, "r")
        contents: str = file.read()
        lines = contents.split(linesep)
        test_results = parser.parse(lines)
        return ParseTestResultResponse(test_results)