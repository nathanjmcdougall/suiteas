"""Test example projects."""

from pathlib import Path
from typing import Self

import pytest

from suiteas.core.run import run_suiteas

valid_projs_dir = Path() / "tests" / "assets" / "valid_projs"
invalid_projs_dir = Path() / "tests" / "assets" / "invalid_projs"


@pytest.fixture(scope="session", params=valid_projs_dir.glob("*"))
def valid_proj_path(request: pytest.FixtureRequest) -> Path:
    """Fixture for valid project directories."""
    return request.param


@pytest.fixture(scope="session")
def valid_proj_posix(valid_proj_path: Path) -> str:
    """Fixture for posix strings to valid project directories."""
    return valid_proj_path.resolve().as_posix()


@pytest.fixture(scope="session", params=invalid_projs_dir.glob("*"))
def invalid_proj_path(request: pytest.FixtureRequest) -> Path:
    """Fixture for invalid project directories."""
    return request.param


@pytest.fixture(scope="session")
def invalid_proj_posix(invalid_proj_path: Path) -> str:
    """Fixture for posix strings to invalid project directories."""
    return invalid_proj_path.resolve().as_posix()


class TestRun:
    def test_is_ok(self: Self, valid_proj_posix: str) -> None:
        """Test that run_suiteas() passes okay."""
        try:
            run_suiteas([valid_proj_posix])
        except SystemExit:
            pytest.fail("SystemExit raised unexpectedly")

    def test_fails(self: Self, invalid_proj_posix: str) -> None:
        """Test that run_suiteas() fails when given an invalid project."""
        with pytest.raises(SystemExit):
            run_suiteas([invalid_proj_posix])
