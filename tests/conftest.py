"""Pytest fixture definitions."""

import pytest


@pytest.fixture(scope="session", params=["example"])
def pkg_name(request: pytest.FixtureRequest) -> str:
    """A package name."""
    return request.param
