"""Functionality for printing to the console."""
import sys

from suiteas.core.violations import Violation


def print_violations(violations: list[Violation]) -> None:
    """Print a list of violations."""
    for violation in violations:
        fmt_info = violation.fmt_info or {}
        msg = (
            f"{violation.rel_path}:{violation.line_num}:{violation.char_offset}: "
            f"{violation.rule.rule_code} "
            f"{violation.rule.description.format(**fmt_info)}"
        )
        print(msg, file=sys.stderr)  # noqa: T201
