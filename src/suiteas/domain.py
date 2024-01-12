"""Value objects for code instances."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.config import ProjConfig


class TestableCodeObject(BaseModel, extra="forbid"):
    """A testable code object."""

    name: str
    full_name: str
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


class File(BaseModel, extra="forbid"):
    """A Python file."""

    path: Path
    funcs: list[Func]
    clses: list[Class]
    imported_objs: list[str]


class Codebase(BaseModel, extra="forbid"):
    """A codebase."""

    files: list[File]


class PytestClass(BaseModel, extra="forbid"):
    """A Pytest test class."""

    name: str
    has_funcs: bool


class PytestFile(BaseModel, extra="forbid"):
    """A Pytest test file."""

    path: Path
    pytest_classes: list[PytestClass]
    imported_objs: list[str]


class PytestSuite(BaseModel, extra="forbid"):
    """A Pytest unit test suite."""

    pytest_files: list[PytestFile]


class Project(BaseModel, extra="forbid"):
    """A Python project."""

    codebase: Codebase
    pytest_suite: PytestSuite
    config: ProjConfig
    proj_dir: Path
