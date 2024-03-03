"""Collect all tests in a directory using pytest."""

from pathlib import Path
from typing import Self

import pytest


class PytestPlugin:
    """Plugin for collecting tests."""

    def __init__(self: Self) -> None:
        """Initialize."""
        self.collected: list[pytest.Item] = []

    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        """Collect all tests."""
        self.collected = items.copy()


def collect_test_items(proj_dir: Path) -> list[pytest.Item]:
    """Collect all tests in a project directory using pytest."""
    if not proj_dir.exists():
        msg = f"Path {proj_dir.as_posix()} does not exist."
        raise FileNotFoundError(msg)

    if not proj_dir.is_dir():
        msg = f"Path {proj_dir.as_posix()} is not a directory."
        raise ValueError(msg)

    plugin = PytestPlugin()
    pytest.main(["--collect-only", "-qq", proj_dir.as_posix()], plugins=[plugin])
    return plugin.collected
