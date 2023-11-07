"""Value objects for code instances."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.config import ProjConfig


class Func(BaseModel):
    """A Python function."""

    name: str


class File(BaseModel):
    """A Python file."""

    path: Path
    funcs: list[Func]


class Codebase(BaseModel):
    """A codebase."""

    files: list[File]


class TestClass(BaseModel):
    """A Pytest test class."""

    name: str


class TestFile(BaseModel):
    """A Pytest test file."""

    path: Path
    test_classes: list[TestClass]


class TestSuite(BaseModel):
    """A Pytest unit test suite."""

    test_files: list[TestFile]


class Project(BaseModel):
    """A Python project."""

    codebase: Codebase
    test_suite: TestSuite
    config: ProjConfig
