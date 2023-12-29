"""Run the suiteas command line interface."""

import sys
from collections.abc import Sequence
from pathlib import Path

from suiteas.core.read.project import get_project
from suiteas.core.validate import is_valid_test_suite


class InvalidTestSuiteError(Exception):
    """An invalid test suite was found."""


def run_suiteas_main(argv: Sequence[str]) -> None:
    """Run the suiteas command line interface without a system exit."""
    if len(argv) == 0:
        proj_dir = "."
    else:
        proj_dir, *_ = argv

    proj_dir = Path(proj_dir).resolve()
    project = get_project(proj_dir)

    if not is_valid_test_suite(project):
        msg = f"Invalid test suite found in {proj_dir}"
        raise InvalidTestSuiteError(msg)


def run_suiteas(argv: Sequence[str] | None = None) -> None:
    """Run the suiteas command line interface."""

    if argv is None:
        argv = []

    try:
        run_suiteas_main(argv)
    except (KeyboardInterrupt, InvalidTestSuiteError):
        sys.exit(1)
