import io
from contextlib import redirect_stderr
from pathlib import Path

from suiteas.core.print import print_violations
from suiteas.core.rules import (
    empty_pytest_class,
    missing_test_func,
    unimported_tested_func,
)
from suiteas.core.violations import Violation


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
                        rule=missing_test_func,
                        rel_path=Path(
                            "src/fakemcfake/example.py",
                        ),
                        line_num=5,
                        char_offset=4,
                        fmt_info=dict(
                            pytest_file_rel_posix="tests/fakemcfake/test_example.py",
                            func="example_func",
                        ),
                    ),
                ],
            )
        s = f.getvalue()
        assert s.replace("\\", "/") == (
            "src/fakemcfake/example.py:5:4: "
            "SUI001 example_func untested in tests/fakemcfake/test_example.py"
            "\n"
        )

    def test_sui002(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations(
                [
                    Violation(
                        rule=empty_pytest_class,
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
        assert s.replace("\\", "/") == (
            "src/fakemcfake/example.py:5:4: SUI002 TestExample has no tests" + "\n"
        )

    def test_sui003(self) -> None:
        f = io.StringIO()
        with redirect_stderr(f):
            print_violations(
                [
                    Violation(
                        rule=unimported_tested_func,
                        rel_path=Path(
                            "src/fakemcfake/example.py",
                        ),
                        line_num=0,
                        char_offset=0,
                        fmt_info=dict(
                            pytest_file_rel_posix="tests/fakemcfake/test_example.py",
                            func_fullname="fakemcfake.example.example_func",
                        ),
                    ),
                ],
            )
        s = f.getvalue()
        assert s.replace("\\", "/") == (
            "src/fakemcfake/example.py:0:0: "
            "SUI003 fakemcfake.example.example_func is not imported "
            "in tests/fakemcfake/test_example.py"
            "\n"
        )
