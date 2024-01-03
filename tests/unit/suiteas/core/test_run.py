from pathlib import Path

import pytest

from suiteas.core.run import run_suiteas_main


class TestRunSuiteAsMain:
    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        with pytest.raises(FileNotFoundError):
            run_suiteas_main([(projs_parent_dir / "no_tests_dir").as_posix()])


class TestPrintViolations:
    def test_nothing(self) -> None:
        assert True


class TestRunSuiteas:
    def test_nothing(self) -> None:
        assert True
