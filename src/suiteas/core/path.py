"""Utilities for manipulating paths."""
from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.core.names import PYTEST_FILE_PREFIX


def path_to_pytest_path(path: Path, *, proj_config: ProjConfig, proj_dir: Path) -> Path:
    """Convert a path to a test path."""
    rel_path = path.relative_to(_get_main_src_dir(proj_config, proj_dir))
    test_parent_path = (
        proj_dir
        / proj_config.tests_rel_path
        / proj_config.unittest_dir_name
        / rel_path.parent
    )
    pytest_path = test_parent_path / f"{PYTEST_FILE_PREFIX}{path.stem}.py"
    return pytest_path


def pytest_path_to_path(
    pytest_path: Path,
    *,
    proj_config: ProjConfig,
    proj_dir: Path,
) -> Path:
    """Convert a test path to a path."""
    rel_path = pytest_path.relative_to(
        proj_dir / proj_config.tests_rel_path / proj_config.unittest_dir_name,
    )
    parent_path = _get_main_src_dir(proj_config, proj_dir) / rel_path.parent

    path = parent_path / rel_path.name.removeprefix(PYTEST_FILE_PREFIX)
    return path


def _get_main_src_dir(proj_config: ProjConfig, proj_dir: Path) -> Path:
    """Get the main source directory."""
    main_src_dir = proj_dir / proj_config.src_rel_path
    if proj_config.use_consolidated_tests_dir:
        (pkg_name,) = proj_config.pkg_names
        main_src_dir /= pkg_name
    return main_src_dir
