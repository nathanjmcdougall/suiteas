"""Functionality for printing to the console."""
import sys

from suiteas.core.check import Violation


def print_violations(violations: list[Violation]) -> None:
    """Print a list of violations."""
    for violation in violations:
        msg = (
            f"{violation.rel_path}:{violation.line_num}:{violation.char_offset}: "
            f"SUI{violation.viol_cat.suiteas_code:03d} "
            f"{violation.viol_cat.description.format(**violation.fmt_info)}"
        )
        print(msg, file=sys.stderr)  # noqa: T201
