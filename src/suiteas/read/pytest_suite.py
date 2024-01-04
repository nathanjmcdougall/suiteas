"""Utilities for reading-in a pytest test suite."""

from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.domain import PytestSuite
from suiteas.read.codebase import _get_module_name
from suiteas.read.pytest_file import get_pytest_file


def get_pytest_suite(
    *,
    proj_dir: Path,
    config: ProjConfig,
    included_pytest_files: list[Path] | None,
) -> PytestSuite:
    """Read the pytest unit test suite for a project."""
    unit_dir = proj_dir / config.tests_rel_path / config.unittest_dir_name

    if not unit_dir.exists():
        msg = f"Could not find {unit_dir}"
        raise FileNotFoundError(msg)

    if included_pytest_files is None:
        included_pytest_files = list(unit_dir.glob("**/*.py"))
    pytest_files = [
        get_pytest_file(
            path,
            module_name=_get_module_name(path=path, root_dir=unit_dir),
        )
        for path in sorted(included_pytest_files)
    ]

    return PytestSuite(pytest_files=pytest_files)
