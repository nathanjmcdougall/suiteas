"""Run the suiteas command line interface."""
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from suiteas.config import ProjConfig
from suiteas.core.validate import is_valid_test_suite
from suiteas.domain import Codebase, Project, PytestSuite

TOML_NAME = "pyproject.toml"


def get_config(proj_dir: Path) -> ProjConfig:
    """Find the configuration for a project."""
    toml_path = proj_dir / TOML_NAME

    if not toml_path.exists():
        msg = f"Could not find {TOML_NAME} in {proj_dir}"
        raise FileNotFoundError(msg)
    with toml_path.open(mode="r") as file:
        pyproject_contents = file.read()
    parsed_toml: dict[str, Any] = tomllib.loads(pyproject_contents)
    config_by_tool: dict[str, Any] = parsed_toml.get("tool", {})
    config_kwargs = config_by_tool.get("suiteas", {})
    config = ProjConfig(**config_kwargs)

    return config


def get_codebase(proj_dir: Path, config: ProjConfig) -> Codebase:
    """Read the codebase for a project."""
    src_dir = proj_dir / config.src_rel_path

    if not src_dir.exists():
        msg = f"Could not find {src_dir} in {proj_dir}"
        raise FileNotFoundError(msg)

    raise NotImplementedError


def get_pytest_suite(proj_dir: Path, config: ProjConfig) -> PytestSuite:
    """Read the pytest suite for a project."""
    _ = proj_dir, config
    raise NotImplementedError


def get_project(proj_dir: Path) -> Project:
    """Get a project from a directory."""
    config = get_config(proj_dir)
    codebase = get_codebase(proj_dir, config)
    pytest_suite = get_pytest_suite(proj_dir, config)

    project = Project(
        codebase=codebase,
        pytest_suite=pytest_suite,
        config=config,
    )
    return project


def _run_suiteas(argv: Sequence[str]) -> None:
    """Run the suiteas command line interface."""
    if len(argv) == 0:
        proj_dir = "."
    else:
        proj_dir, *_ = argv

    proj_dir = Path(proj_dir).resolve()
    project = get_project(proj_dir)

    if not is_valid_test_suite(project):
        sys.exit(1)


def run_suiteas(argv: Sequence[str] | None = None) -> None:
    """Run the suiteas command line interface."""

    if argv is None:
        raise NotImplementedError

    try:
        _run_suiteas(argv)
    except KeyboardInterrupt:
        sys.exit(1)
