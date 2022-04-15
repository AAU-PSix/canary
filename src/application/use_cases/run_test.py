from typing import IO, Any, Union
from .use_case import *
from .run_subprocess import *

class RunTestRequest(UseCaseRequest):
    def __init__(
        self,
        build_command: str,
        test_command: str,
        test_stdout: Union[str, IO[Any]] = None,
    ) -> None:
        self._build_command = build_command
        self._test_command = test_command
        self._test_stdout = test_stdout
        super().__init__()

    @property
    def build_command(self) -> str:
        return self._build_command

    @property
    def test_command(self) -> str:
        return self._test_command

    @property
    def test_stdout(self) -> Union[str, IO[Any]]:
        return self._test_stdout

class RunTestResponse(UseCaseResponse): pass

class RunTestUseCase(
    UseCase[RunTestRequest, RunTestResponse]
):
    def do(self, request: RunTestRequest) -> RunTestResponse:
        # If the stdout is a string, then create the output file
        if isinstance(request.test_stdout, str):
            test_output = open(request.test_stdout, 'w')
        else: test_output = request.test_stdout

        runner = RunSubsystemUseCase()
        build_request = RunSubsystemRequest(
            request.build_command
        )
        test_request = RunSubsystemRequest(
            request.test_command, stdout=test_output
        )

        runner.do(build_request)
        runner.do(test_request)

        test_output.close()

        return RunTestResponse()
