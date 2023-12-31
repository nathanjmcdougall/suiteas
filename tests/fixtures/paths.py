"""Fixtures for testing project directories."""
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def root_dir() -> Path:
    """Fixture for valid project directories."""
    return ROOT_DIR


@pytest.fixture(scope="session")
def test_assets_dir(root_dir: Path) -> Path:
    """Fixture for valid project directories."""
    return root_dir / "tests" / "assets"


@pytest.fixture(scope="session")
def projs_parent_dir(test_assets_dir: Path) -> Path:
    """Fixture for a directory containing Python project folders."""
    return test_assets_dir / "projects"


@pytest.fixture(scope="session")
def files_parent_dir(test_assets_dir: Path) -> Path:
    """Fixture for a directory containing Python files."""
    return test_assets_dir / "files"


@pytest.fixture(scope="session")
def config_files_parent_dir(test_assets_dir: Path) -> Path:
    """Fixture for a directory with TOML pyproject.toml style configuration files."""
    return test_assets_dir / "config_files"
