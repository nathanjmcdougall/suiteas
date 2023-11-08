"""TestFile instances for testing purposes."""
from pathlib import Path

from suiteas.domain import (
    PytestClass,
    PytestFile,
)


def null_pytest_file(path: Path) -> PytestFile:
    """A file with no Pytest classes at the given path."""
    return PytestFile(path=path, pytest_classes=[])


def oneclass_pytest_file(path: Path, pytest_class_name: str) -> PytestFile:
    """A file with a single Pytest class at the given path, with the given name."""
    pytest_class = PytestClass(name=pytest_class_name)
    return PytestFile(path=path, pytest_classes=[pytest_class])
