from typing import IO, Any, Union
from .use_case import *
from .run_subprocess import *

class RunTestRequest(UseCaseRequest):
    def __init__(
        self,
        build_command: str,
        test_command: str,
        out: Union[str, IO[Any]] = None,
    ) -> None:
        self._build_command = build_command
        self._test_command = test_command
        self._out = out
        super().__init__()

    @property
    def build_command(self) -> str:
        return self._build_command

    @property
    def test_command(self) -> str:
        return self._test_command

    @property
    def out(self) -> Union[str, IO[Any]]:
        return self._out

class RunTestResponse(UseCaseResponse): pass

class RunTestUseCase(
    UseCase[RunTestRequest, RunTestResponse]
):
    def do(self, request: RunTestRequest) -> RunTestResponse:
        # If the stdout is a string, then create the output file
        if isinstance(request.out, str):
            test_output = open(request.out, 'w+')
        else: test_output = request.out

        runner = RunSubsystemUseCase()
        if request.build_command is not None:
            build_request = RunSubsystemRequest(
                request.build_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            runner.do(build_request)

        test_request = RunSubsystemRequest(
            request.test_command,
            stdout=test_output,
            stderr=test_output,
        )
        runner.do(test_request)

        test_output.close()

        return RunTestResponse()
