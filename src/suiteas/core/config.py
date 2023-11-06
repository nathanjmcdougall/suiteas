"""Configuration for the package to be analyzed."""

from pathlib import Path

from pydantic import BaseModel


class PkgConfig(BaseModel):
    """Configuration for the package to be analyzed."""

    pkg_names: list[str]
    tests_rel_path: Path = "tests"
    src_rel_path: Path = "src"
    unittest_dir_name: str = "unit"
