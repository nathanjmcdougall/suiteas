"""Value objects for code objects."""

from pathlib import Path

from pydantic import BaseModel


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
    """A pytest test class."""
    name: str

class TestFile(BaseModel):
    """A pytest test file."""
    path: Path
    test_classes: list[TestClass]

class TestSuite(BaseModel):
    """A pytest unit test suite."""
    test_files: list[TestFile]
