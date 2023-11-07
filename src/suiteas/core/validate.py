"""Functionality to check whether a test suite is validly organized."""

from suiteas.config import ProjConfig
from suiteas.core.organize import organize_test_suite
from suiteas.domain import Codebase, TestSuite


def is_valid_test_suite(
    codebase: Codebase,
    test_suite: TestSuite,
    proj_config: ProjConfig,
) -> bool:
    """Validate a test suite."""
    new_test_suite = organize_test_suite(codebase, test_suite, proj_config)
    return new_test_suite == test_suite
