"""Value objects for code instances."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.config import ProjConfig


class CodeObject(BaseModel, extra="forbid"):
    """A code object."""

    name: str
    full_name: str
    line_num: int
    char_offset: int

    @property
    def is_underscored(self) -> bool:
        """Return whether the object's name starts with an underscore."""
        return self.name.startswith("_")


class Decorator(BaseModel, extra="forbid"):
    """A Python decorator."""

    line_num: int


class Func(CodeObject):
    """A general Python function."""

    decs: list[Decorator]


class Class(CodeObject):
    """A general Python class."""

    funcs: list[Func]


class File(BaseModel, extra="forbid"):
    """A general Python file."""

    path: Path
    funcs: list[Func]
    clses: list[Class]
    imported_objs: list[str]


class Codebase(BaseModel, extra="forbid"):
    """A Python codebase."""

    files: list[File]


class PytestFunc(Func):
    """A Pytest test function."""

    is_collected: bool  # i.e. collected by pytest as a test


class PytestClass(Class):
    """A Pytest test class."""

    pytest_funcs: list[PytestFunc]


class PytestFile(File):
    """A Pytest test file."""

    lone_pytest_funcs: list[PytestFunc]
    pytest_clses: list[PytestClass]


class PytestSuite(BaseModel, extra="forbid"):
    """A Pytest unit test suite."""

    pytest_files: list[PytestFile]


class Project(BaseModel, extra="forbid"):
    """A Python project."""

    codebase: Codebase
    pytest_suite: PytestSuite
    config: ProjConfig
    proj_dir: Path
