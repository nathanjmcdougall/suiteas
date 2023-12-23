"""Value objects for code instances."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.config import ProjConfig


class Func(BaseModel):
    """A Python function."""

    name: str

    @property
    def is_underscored(self) -> bool:
        """Return whether the function name starts with an underscore."""
        return self.name.startswith("_")


class File(BaseModel):
    """A Python file."""

    path: Path
    funcs: list[Func]


class Codebase(BaseModel):
    """A codebase."""

    files: list[File]


class PytestClass(BaseModel):
    """A Pytest test class."""

    name: str


class PytestFile(BaseModel):
    """A Pytest test file."""

    path: Path
    pytest_classes: list[PytestClass]


class PytestSuite(BaseModel):
    """A Pytest unit test suite."""

    pytest_files: list[PytestFile]


class Project(BaseModel):
    """A Python project."""

    codebase: Codebase
    pytest_suite: PytestSuite
    config: ProjConfig
