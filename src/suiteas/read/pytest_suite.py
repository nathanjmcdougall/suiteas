"""Utilities for reading-in a pytest test suite."""

from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.domain import PytestSuite
from suiteas.read.codebase import _get_module_name
from suiteas.read.pytest_collect import collect_test_items
from suiteas.read.pytest_file import get_pytest_file


def get_pytest_suite(
    *,
    proj_dir: Path,
    config: ProjConfig,
    included_pytest_files: list[Path] | None,
    is_static_only: bool = False,
) -> PytestSuite:
    """Read the pytest unit test suite for a project."""
    unit_dir = proj_dir / config.tests_rel_path / config.unittest_dir_name

    pytest_items = collect_test_items(proj_dir=proj_dir) if not is_static_only else []

    if not unit_dir.exists():
        msg = f"Could not find {unit_dir}"
        raise FileNotFoundError(msg)

    if included_pytest_files is None:
        included_pytest_files = list(unit_dir.glob("**/*.py"))
    pytest_files = [
        get_pytest_file(
            path,
            module_name=_get_module_name(path=path, root_dir=unit_dir),
            pytest_items=pytest_items,
        )
        for path in sorted(included_pytest_files)
    ]

    return PytestSuite(pytest_files=pytest_files)
