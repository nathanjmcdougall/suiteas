"""Utilities for reading-in a Python codebase."""
from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.core.read.file import get_file
from suiteas.domain import Codebase


def get_codebase(proj_dir: Path, config: ProjConfig) -> Codebase:
    """Read the codebase for a project."""
    src_dir = proj_dir / config.src_rel_path

    if not src_dir.exists():
        msg = f"Could not find {src_dir}"
        raise FileNotFoundError(msg)

    files = [get_file(path) for path in src_dir.glob("**/*.py")]
    files.sort()

    return Codebase(files=files)
