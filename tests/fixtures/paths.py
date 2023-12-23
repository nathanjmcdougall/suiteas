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
    """Fixture for valid project directories."""
    return test_assets_dir / "projects"


@pytest.fixture(scope="session")
def files_parent_dir(test_assets_dir: Path) -> Path:
    """Fixture for valid project directories."""
    return test_assets_dir / "files"
