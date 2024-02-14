"""Utilities for recording violations of the test suite rules."""

from pathlib import Path

from pydantic import BaseModel

from suiteas.core.rules import Rule


class Violation(BaseModel):
    """A violation of the test suite rules."""

    rule: Rule
    rel_path: Path
    line_num: int = 0
    char_offset: int = 0
    fmt_info: dict[str, str] | None = None
