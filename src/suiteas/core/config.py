"""Configuration for the package to be analyzed."""

from pathlib import Path

from pydantic import BaseModel


class PkgConfig(BaseModel):
    """Configuration for the package to be analyzed."""

    tests_rel_path: Path
    src_rel_path: Path
    pkg_names: list[str]



