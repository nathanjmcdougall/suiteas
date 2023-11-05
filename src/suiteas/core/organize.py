"""Core organization functionality."""
from suiteas.domain.codeobj import Codebase, TestSuite


def organize_test_suite(codebase: Codebase, test_suite: TestSuite) -> TestSuite:
    """Organize a codebase into a corresponding test suite."""
    _ = codebase
    return test_suite
