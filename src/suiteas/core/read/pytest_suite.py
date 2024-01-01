"""Utilities for reading-in a pytest test suite."""

from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.core.read.pytest_file import get_pytest_file
from suiteas.domain import PytestSuite


def get_pytest_suite(proj_dir: Path, config: ProjConfig) -> PytestSuite:
    """Read the pytest unit test suite for a project."""
    unit_dir = proj_dir / config.tests_rel_path / config.unittest_dir_name

    if not unit_dir.exists():
        msg = f"Could not find {unit_dir}"
        raise FileNotFoundError(msg)

    pytest_files = [get_pytest_file(path) for path in unit_dir.glob("**/*.py")]

    return PytestSuite(pytest_files=pytest_files)
