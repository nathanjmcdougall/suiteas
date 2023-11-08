"""Functionality to check whether a test suite is validly organized."""

from suiteas.config import ProjConfig
from suiteas.core.organize import organize_test_suite
from suiteas.domain import Codebase, PytestSuite


def is_valid_test_suite(
    codebase: Codebase,
    pytest_suite: PytestSuite,
    proj_config: ProjConfig,
) -> bool:
    """Validate a test suite."""
    new_pytest_suite = organize_test_suite(codebase, pytest_suite, proj_config)
    return new_pytest_suite == pytest_suite
