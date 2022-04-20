class TestSummary():
    def __init__(
        self,
        test_count: int,
        failure_count: int,
        success_count: int
    ) -> None:
        self._test_count = test_count
        self._failure_count = failure_count
        self._success_count = success_count

    @property
    def test_count(self) -> int:
        return self._test_count

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def success_count(self) -> int:
        return self._success_count