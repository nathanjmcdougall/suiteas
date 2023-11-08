"""TestSuite instances for testing purposes."""
from pathlib import Path

from suiteas.domain import (
    PytestSuite,
)
from suiteas_test.test_file import null_pytest_file, oneclass_pytest_file


def empty_test_suite() -> PytestSuite:
    """An empty test suite."""
    return PytestSuite(pytest_files=[])


def null_file_test_suite(path: Path) -> PytestSuite:
    """A test suite with a single file (at the given path) with no test classes."""
    return PytestSuite(pytest_files=[null_pytest_file(path=path)])


def oneclass_file_testsuite(path: Path, test_class_name: str) -> PytestSuite:
    """A test suite with a single file (at the given path) with a single test class."""
    return PytestSuite(
        pytest_files=[
            oneclass_pytest_file(path=path, pytest_class_name=test_class_name),
        ],
    )
