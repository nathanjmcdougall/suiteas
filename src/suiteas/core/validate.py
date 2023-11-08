"""Functionality to check whether a test suite is validly organized."""

from suiteas.core.organize import organize_test_suite
from suiteas.domain import Project


def is_valid_test_suite(project: Project) -> bool:
    """Validate a test suite."""
    new_pytest_suite = organize_test_suite(project)
    return new_pytest_suite == project.pytest_suite
