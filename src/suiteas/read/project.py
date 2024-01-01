"""Utilities to reading-in a Python project."""

from pathlib import Path

from suiteas.core.read.codebase import get_codebase
from suiteas.core.read.config import get_config
from suiteas.core.read.pytest_suite import get_pytest_suite
from suiteas.domain import Project

TOML_NAME = "pyproject.toml"


def get_project(proj_dir: Path) -> Project:
    """Get a project from a directory."""
    config = get_config(proj_dir)
    codebase = get_codebase(proj_dir, config)
    pytest_suite = get_pytest_suite(proj_dir, config)

    project = Project(
        codebase=codebase,
        pytest_suite=pytest_suite,
        config=config,
    )
    return project
