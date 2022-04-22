import subprocess
from typing import IO, Any
from .use_case import *

class RunSubsystemRequest(UseCaseRequest):
    def __init__(
        self,
        command: str,
        input: Any = None,
        capture_output: bool = False,
        timeout: int = None,
        check: bool = False,
        stdin: IO[Any] = None,
        stdout: IO[Any] = None,
        stderr: IO[Any] = None,
    ) -> None:
        self._command = command
        self._input = input
        self._capture_output = capture_output
        self._timeout = timeout
        self._check = check
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        super().__init__()

    @property
    def command(self) -> str:
        return self._command

    @property
    def input(self) -> Any:
        return self._input

    @property
    def capture_output(self) -> bool:
        return self._capture_output

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def check(self) -> bool:
        return self._check

    @property
    def stdin(self) -> IO[Any]:
        return self._stdin

    @property
    def stdout(self) -> IO[Any]:
        return self._stdout

    @property
    def stderr(self) -> IO[Any]:
        return self._stderr

class RunSubsystemResponse(UseCaseResponse): pass

class RunSubsystemUseCase(
    UseCase[RunSubsystemRequest, RunSubsystemResponse]
):
    def do(self, request: RunSubsystemRequest) -> RunSubsystemResponse:
        subprocess.run(
            # If we dont split it will attempt to open it as a file
            request.command.split(),
            stdout=request.stdout,
            stderr=request.stderr,
            timeout=10
        )
        return RunSubsystemResponse()
