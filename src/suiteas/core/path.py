"""Utilities for manipulating paths."""
from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.core.pytest import TEST_FILE_PREFIX


def path_to_test_path(path: Path, *, proj_config: ProjConfig, proj_dir: Path) -> Path:
    """Convert a path to a test path."""
    rel_path = path.relative_to(proj_dir / proj_config.src_rel_path)
    test_parent_path = (
        proj_config.tests_rel_path / proj_config.unittest_dir_name / rel_path.parent
    )
    test_path = test_parent_path / f"{TEST_FILE_PREFIX}{path.stem}.py"
    return test_path


def test_path_to_path(
    test_path: Path,
    *,
    proj_config: ProjConfig,
    proj_dir: Path,
) -> Path:
    """Convert a test path to a path."""
    rel_path = test_path.relative_to(
        proj_dir / proj_config.tests_rel_path / proj_config.unittest_dir_name,
    )
    parent_path = proj_config.src_rel_path / rel_path.parent
    path = parent_path / rel_path.name.removeprefix(TEST_FILE_PREFIX)
    return path
