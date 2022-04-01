
from typing import List
from cutest_parser import CuTestParser, FailedCuTest
from .use_case import *


class ParseTestResultRequest(UseCaseRequest):
    def __init__(
        self,
        test_result_file_path: str
    ) -> None:
        self._test_result_file_path = test_result_file_path
        super().__init__()

    @property
    def test_result_file_path(self) -> str:
        return self._test_result_file_path


class ParseTestResultResponse(UseCaseResponse): 
    def __init__(
        self, 
        test_result
    ) -> None:
        self._test_results: List[FailedCuTest] = test_result
        super().__init__()
    
    @property
    def test_results(self) -> List[FailedCuTest]:
        return self._test_results

class ParseTestResultUseCase(
    UseCase[ParseTestResultRequest, ParseTestResultResponse]
):  
    def do(self, request: ParseTestResultRequest) -> ParseTestResultResponse:
        test_result_parser = CuTestParser()
        test_result_file = test_result_parser.read_parse_file(request._test_result_file_path)
        test_results = test_result_parser.parse(test_result_file)

        return ParseTestResultResponse(test_results)