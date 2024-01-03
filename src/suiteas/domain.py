"""Value objects for code instances."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.config import ProjConfig


class TestableCodeObject(BaseModel):
    """A testable code object."""

    name: str
    line_num: int
    char_offset: int

    @property
    def is_underscored(self) -> bool:
        """Return whether the object's name starts with an underscore."""
        return self.name.startswith("_")


class Class(TestableCodeObject):
    """A Python class."""

    has_funcs: bool


class Func(TestableCodeObject):
    """A Python function."""


class File(BaseModel):
    """A Python file."""

    path: Path
    funcs: list[Func]
    clses: list[Class]


class Codebase(BaseModel):
    """A codebase."""

    files: list[File]


class PytestClass(BaseModel):
    """A Pytest test class."""

    name: str
    has_funcs: bool


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
    proj_dir: Path
