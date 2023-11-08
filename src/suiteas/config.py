"""Configuration for the Python project to be analyzed."""

from pathlib import Path

from pydantic import BaseModel


class ProjConfig(BaseModel):
    """Configuration for the Python project to be analyzed."""

    pkg_names: list[str]
    src_rel_path: Path = "src"
    tests_rel_path: Path = "tests"
    unittest_dir_name: str = "unit"
