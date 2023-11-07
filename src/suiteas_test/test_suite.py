"""TestSuite instances for testing purposes."""
from pathlib import Path

from suiteas.domain import (
    TestSuite,
)
from suiteas_test.test_file import null_test_file, oneclass_test_file


def empty_test_suite() -> TestSuite:
    """An empty test suite."""
    return TestSuite(test_files=[])


def null_file_test_suite(path: Path) -> TestSuite:
    """A test suite with a single file (at the given path) with no test classes."""
    return TestSuite(test_files=[null_test_file(path=path)])


def oneclass_file_testsuite(path: Path, test_class_name: str) -> TestSuite:
    """A test suite with a single file (at the given path) with a single test class."""
    return TestSuite(
        test_files=[oneclass_test_file(path=path, test_class_name=test_class_name)],
    )
