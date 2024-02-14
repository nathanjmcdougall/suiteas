import os
from pathlib import Path

import pytest

from suiteas.core.run import run_suiteas, run_suiteas_main


class TestRunSuiteAsMain:
    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        old_cwd = Path.cwd()
        os.chdir(projs_parent_dir / "no_tests_dir")
        with pytest.raises(FileNotFoundError):
            run_suiteas_main([])
        os.chdir(old_cwd)


class TestRunSuiteAs:
    def test_nothing(self) -> None:
        _ = run_suiteas
