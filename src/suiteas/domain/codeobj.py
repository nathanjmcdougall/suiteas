"""Value objects for code objects."""

from pydantic import BaseModel


class Function(BaseModel):
    """A Python function."""
    name: str

class File(BaseModel):
    """A Python file."""
    name: str
    functions: list[Function]

class Codebase(BaseModel):
    """A codebase."""
    files: list[File]

class TestClass(BaseModel):
    """A pytest test class."""
    name: str

class TestFile(BaseModel):
    """A pytest test file."""
    name: str
    test_classes: list[TestClass]

class TestSuite(BaseModel):
    """A pytest unit test suite."""
    files: list[TestFile]
