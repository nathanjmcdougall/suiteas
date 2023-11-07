"""TestFile instances for testing purposes."""
from pathlib import Path

from suiteas.domain import (
    TestClass,
    TestFile,
)


def null_test_file(path: Path) -> TestFile:
    """A file with no test classes at the given path."""
    return TestFile(path=path, test_classes=[])


def oneclass_test_file(path: Path, test_class_name: str) -> TestFile:
    """A file with a single test class at the given path, with the given name."""
    test_class = TestClass(name=test_class_name)
    return TestFile(path=path, test_classes=[test_class])
