"""Utilities for reading-in a pytest test file."""

from pathlib import Path

from suiteas.core.names import PYTEST_CLASS_PREFIX
from suiteas.domain import Class, PytestClass, PytestFile
from suiteas.read.file import get_file


def get_pytest_file(path: Path, *, module_name: str) -> PytestFile:
    """Read a pytest test file."""
    file = get_file(path, module_name=module_name)
    pytest_classes = [
        PytestClass(
            name=cls.name,
            has_funcs=cls.has_funcs,
        )
        for cls in file.clses
        if _is_pytest_class(cls)
    ]
    return PytestFile(
        path=file.path,
        pytest_classes=pytest_classes,
        imported_objs=file.imported_objs,
    )


def _is_pytest_class(cls: Class) -> bool:
    """Check if a class is a pytest class."""
    return cls.name.startswith(PYTEST_CLASS_PREFIX)
