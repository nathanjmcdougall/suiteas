from suiteas.read.pytest_suite import get_pytest_suite


class TestGetPytestSuite:
    def test_nothing(self) -> None:
        _ = get_pytest_suite
