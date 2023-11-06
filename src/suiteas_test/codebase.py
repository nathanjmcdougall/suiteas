"""Codebase instances for testing purposes."""
from pathlib import Path

from suiteas.domain.codeobj import (
    Codebase,
)
from suiteas_test.file import null_file, onefunc_file


def empty_codebase() -> Codebase:
    """An empty codebase."""
    return Codebase(files=[])


def null_file_codebase(path: Path) -> Codebase:
    """A codebase with a single file (at the given path) with no functions."""
    return Codebase(files=[null_file(path=path)])


def onefunc_file_codebase(path: Path, func_name: str) -> Codebase:
    """A codebase with a single file (at the given path) with a single function."""
    return Codebase(files=[onefunc_file(path=path, func_name=func_name)])
