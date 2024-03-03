"""Run the suiteas command line interface."""

import sys
from collections.abc import Sequence
from pathlib import Path

from suiteas.core.check import get_violations
from suiteas.core.names import PYPROJTOML_NAME
from suiteas.core.print import print_violations
from suiteas.read.project import get_project

MAX_PROJ_DIR_DEPTH = 1000


def run_suiteas_main(argv: Sequence[str]) -> None:
    """Run the suiteas command line interface without a system exit."""
    argv = list(argv)

    is_static_only = "--static-only" in argv
    if is_static_only:
        argv.remove("--static-only")

    included_files = [Path(arg) for arg in argv if not arg.startswith("--")]
    bad_flags = [arg for arg in argv if arg.startswith("--")]

    _report_bad_flags(bad_flags)

    proj_dir = _infer_proj_dir()
    project = get_project(
        proj_dir=proj_dir,
        included_files=included_files,
        is_static_only=is_static_only,
    )

    violations = get_violations(project)
    if violations:
        print_violations(violations)
        sys.exit(1)


def _report_bad_flags(bad_flags: list[str]) -> None:
    if bad_flags:
        msg = f"Unrecognized flags {" ".join(bad_flags)} provided"
        raise ValueError(msg)


def run_suiteas(argv: Sequence[str] | None = sys.argv) -> None:
    """Run the suiteas command line interface."""

    if argv is None:
        argv = []

    if len(sys.argv) == 1:
        argv = []
    elif len(sys.argv) > 1:
        argv = sys.argv[1:]
    else:
        raise AssertionError

    try:
        run_suiteas_main(argv)
    except KeyboardInterrupt:
        sys.exit(1)


INFER_PROJ_DIR_FAIL_MSG = "Could not infer the project directory for the project."


def _infer_proj_dir() -> Path:
    candidate_dir = Path.cwd().resolve()
    for _ in range(MAX_PROJ_DIR_DEPTH):
        if (candidate_dir / PYPROJTOML_NAME).is_file():
            return candidate_dir

        if (
            (candidate_dir / ".git").is_dir()
            or (candidate_dir / ".hg").is_dir()
            or (candidate_dir / ".svn").is_dir()
        ):
            return candidate_dir

        if candidate_dir.parent == candidate_dir:
            raise ValueError(INFER_PROJ_DIR_FAIL_MSG)

        candidate_dir = candidate_dir.parent

    raise ValueError(INFER_PROJ_DIR_FAIL_MSG)
