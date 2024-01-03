"""Utilities for reading-in a Python codebase."""
from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.domain import Codebase
from suiteas.read.file import get_file


def get_codebase(
    *,
    proj_dir: Path,
    config: ProjConfig,
    included_src_files: list[Path] | None = None,
) -> Codebase:
    """Read the codebase for a project."""
    src_dir = proj_dir / config.src_rel_path

    if not src_dir.exists():
        msg = f"Could not find {src_dir}"
        raise FileNotFoundError(msg)

    if included_src_files is None:
        included_src_files = list(src_dir.glob("**/*.py"))
    files = [
        get_file(
            path,
            module_name=_get_module_name(path=path, root_dir=src_dir),
        )
        for path in sorted(included_src_files)
    ]

    return Codebase(files=files)


def _get_module_name(*, path: Path, root_dir: Path) -> str:
    return (
        path.relative_to(root_dir)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
        .replace(".__init__", "")
    )
