"""Utilities for recording violations of the test suite rules."""


from pathlib import Path

from pydantic import BaseModel


class ViolationCategory(BaseModel):
    """A category of violation."""

    suiteas_code: int
    name: str
    description: str


class Violation(BaseModel):
    """A violation of the test suite rules."""

    viol_cat: ViolationCategory
    rel_path: Path
    line_num: int = 0
    char_offset: int = 0
    fmt_info: dict[str, str] | None = None


missing_test_func = ViolationCategory(
    suiteas_code=1,
    name="missing-test-func",
    description="{func} untested in {pytest_file_rel_posix}",
)
