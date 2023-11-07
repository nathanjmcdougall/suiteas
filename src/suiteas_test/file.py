"""File instances for testing purposes."""
from pathlib import Path

from suiteas.domain import File, Func


def null_file(path: Path) -> File:
    """A file with no functions at the given path."""
    return File(path=path, funcs=[])


def onefunc_file(path: Path, func_name: str) -> File:
    """A file with a single function at the given path."""
    func = Func(name=func_name)
    return File(path=path, funcs=[func])
