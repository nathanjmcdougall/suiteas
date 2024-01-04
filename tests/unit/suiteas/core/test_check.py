from suiteas.core.check import get_violations


class TestGetViolations:
    def test_nothing(self) -> None:
        _ = get_violations
