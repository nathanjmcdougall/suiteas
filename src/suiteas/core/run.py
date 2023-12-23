"""Run the suiteas command line interface."""

import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from suiteas.config import ProjConfig
from suiteas.core.read.file import get_file
from suiteas.core.validate import is_valid_test_suite
from suiteas.domain import Codebase, Project, PytestFile, PytestSuite

TOML_NAME = "pyproject.toml"


class InvalidTestSuiteError(Exception):
    """An invalid test suite was found."""


class ConfigFileError(ValueError):
    """An invalid configuration file was found."""


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
    if not config_kwargs:
        msg = f"Could not find [tool.suiteas] configuration section in {TOML_NAME}"
        raise ConfigFileError(msg)
    config = ProjConfig(**config_kwargs)

    return config


def get_codebase(proj_dir: Path, config: ProjConfig) -> Codebase:
    """Read the codebase for a project."""
    src_dir = proj_dir / config.src_rel_path

    if not src_dir.exists():
        msg = f"Could not find {src_dir}"
        raise FileNotFoundError(msg)

    files = [get_file(path) for path in src_dir.glob("**/*.py")]

    return Codebase(files=files)


def get_pytest_suite(proj_dir: Path, config: ProjConfig) -> PytestSuite:
    """Read the pytest unit test suite for a project."""
    unit_dir = proj_dir / config.tests_rel_path / config.unittest_dir_name

    if not unit_dir.exists():
        msg = f"Could not find {unit_dir}"
        raise FileNotFoundError(msg)

    pytest_files = [get_pytest_file(path) for path in unit_dir.glob("**/*.py")]

    return PytestSuite(pytest_files=pytest_files)


def get_pytest_file(path: Path) -> PytestFile:
    """Read a pytest test file."""
    return PytestFile(path=path, pytest_classes=[])


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


def run_suiteas_main(argv: Sequence[str]) -> None:
    """Run the suiteas command line interface without a system exit."""
    if len(argv) == 0:
        proj_dir = "."
    else:
        proj_dir, *_ = argv

    proj_dir = Path(proj_dir).resolve()
    project = get_project(proj_dir)

    if not is_valid_test_suite(project):
        msg = f"Invalid test suite found in {proj_dir}"
        raise InvalidTestSuiteError(msg)


def run_suiteas(argv: Sequence[str] | None = None) -> None:
    """Run the suiteas command line interface."""

    if argv is None:
        argv = []

    try:
        run_suiteas_main(argv)
    except (KeyboardInterrupt, InvalidTestSuiteError):
        sys.exit(1)
