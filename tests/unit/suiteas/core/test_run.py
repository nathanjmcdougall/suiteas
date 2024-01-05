import io
import os
from contextlib import redirect_stderr
from pathlib import Path

import pytest

from suiteas.core.run import print_violations, run_suiteas, run_suiteas_main
from suiteas.core.violations import (
    Violation,
    empty_pytest_class,
    missing_test_func,
    unimported_tested_func,
)


class TestRunSuiteAsMain:
    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        old_cwd = Path.cwd()
        os.chdir(projs_parent_dir / "no_tests_dir")
        with pytest.raises(FileNotFoundError):
            run_suiteas_main([])
        os.chdir(old_cwd)


class TestPrintViolations:
    def test_no_violations(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations([])
        s = f.getvalue()
        assert s == ""

    def test_sui001(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations(
                [
                    Violation(
                        viol_cat=missing_test_func,
                        rel_path=Path(
                            "src/fakemcfake/example.py",
                        ),
                        line_num=5,
                        char_offset=4,
                        fmt_info=dict(
                            pytest_file_rel_posix=r"tests\fakemcfake\test_example.py",
                            func="example_func",
                        ),
                    ),
                ],
            )
        s = f.getvalue()
        assert s == (
            r"src\fakemcfake\example.py:5:4: "
            r"SUI001 example_func untested in tests\fakemcfake\test_example.py"
            "\n"
        )

    def test_sui002(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations(
                [
                    Violation(
                        viol_cat=empty_pytest_class,
                        rel_path=Path(
                            "src/fakemcfake/example.py",
                        ),
                        line_num=5,
                        char_offset=4,
                        fmt_info=dict(pytest_class_name="TestExample"),
                    ),
                ],
            )
        s = f.getvalue()
        assert s == (
            r"src\fakemcfake\example.py:5:4: SUI002 TestExample has no tests" + "\n"
        )

    def test_sui003(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations(
                [
                    Violation(
                        viol_cat=unimported_tested_func,
                        rel_path=Path(
                            "src/fakemcfake/example.py",
                        ),
                        line_num=0,
                        char_offset=0,
                        fmt_info=dict(
                            pytest_file_rel_posix=r"tests\fakemcfake\test_example.py",
                            func_fullname="fakemcfake.example.example_func",
                        ),
                    ),
                ],
            )
        s = f.getvalue()
        assert s == (
            r"src\fakemcfake\example.py:0:0: "
            r"SUI003 fakemcfake.example.example_func is not imported "
            r"in tests\fakemcfake\test_example.py"
            "\n"
        )


class TestRunSuiteAs:
    def test_nothing(self) -> None:
        _ = run_suiteas
