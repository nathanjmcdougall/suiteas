"""Utilities for reading-in a pytest test file."""

from pathlib import Path

from suiteas.core.pytest import TEST_CLASS_PREFIX
from suiteas.core.read.file import get_file
from suiteas.domain import Class, PytestClass, PytestFile


def get_pytest_file(path: Path) -> PytestFile:
    """Read a pytest test file."""
    file = get_file(path)
    pytest_classes = [
        PytestClass(name=cls.name) for cls in file.clses if _is_pytest_class(cls)
    ]
    return PytestFile(path=file.path, pytest_classes=pytest_classes)


def _is_pytest_class(cls: Class) -> bool:
    """Check if a class is a pytest class."""
    return cls.name.startswith(TEST_CLASS_PREFIX)
