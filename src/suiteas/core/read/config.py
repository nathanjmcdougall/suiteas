"""Utilities for reading a project's configuration."""
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from suiteas.config import ProjConfig

TOML_NAME = "pyproject.toml"


class ConfigFileError(ValueError):
    """An invalid configuration file was found."""


def get_config(proj_dir: Path) -> ProjConfig:
    """Find the configuration for a project in the pyproject.toml file."""
    toml_path = proj_dir / TOML_NAME
    toml_config = get_toml_config(toml_path)

    pkg_names = (
        toml_config.pkg_names
        if toml_config.pkg_names is not None
        else toml_config.setuptools_pkg_names
    )
    src_rel_path = toml_config.src_rel_path
    tests_rel_path = toml_config.tests_rel_path
    unittest_dir_name = toml_config.unittest_dir_name

    if src_rel_path is None:
        src_rel_path = _heuristic_src_rel_path(proj_dir, pkg_names)

    src_path = proj_dir / src_rel_path
    if not src_path.exists():
        msg = f"Could not find source directory {src_path}"
        raise FileNotFoundError(msg)

    if pkg_names is None:
        pkg_names = _heuristic_pkg_names(proj_dir, src_rel_path)

    if tests_rel_path is None:
        tests_rel_path = _heuristic_test_rel_path(proj_dir)

    tests_path = proj_dir / tests_rel_path
    if not tests_path.exists():
        msg = f"Could not find tests directory {tests_path}"
        raise FileNotFoundError(msg)

    if unittest_dir_name is None:
        unittest_dir_name = _heuristic_unittest_dir_name(tests_path)

    return ProjConfig(
        pkg_names=pkg_names,
        src_rel_path=src_rel_path,
        tests_rel_path=tests_rel_path,
        unittest_dir_name=unittest_dir_name,
    )


def _heuristic_src_rel_path(proj_dir: Path, pkg_names: list[str] | None) -> Path:
    if (proj_dir / "src").exists():
        return Path("src")

    if pkg_names is not None and all(
        (proj_dir / pkg_name).exists() for pkg_name in pkg_names
    ):
        return Path(".")
    msg = (
        "Could not automatically determine source directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'src_rel_path = "???"'
    )
    raise ConfigFileError(msg)


def _heuristic_pkg_names(proj_dir: Path, src_rel_path: Path) -> list[str]:
    if src_rel_path != Path("."):
        return [
            path.name for path in (proj_dir / src_rel_path).glob("*") if path.is_dir()
        ]

    msg = (
        "Could not automatically determine package names for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'pkg_names = ["???"]'
    )
    raise ConfigFileError(msg)


def _heuristic_test_rel_path(proj_dir: Path) -> Path:
    if (proj_dir / "tests").exists():
        return Path("tests")
    if (proj_dir / "test").exists():
        return Path("test")
    if (proj_dir / "testing").exists():
        return Path("testing")

    msg = (
        "Could not automatically determine tests directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'tests_rel_path = "???"'
    )
    raise ConfigFileError(msg)


def _heuristic_unittest_dir_name(tests_path: Path) -> Path:
    if (tests_path / "unit").exists():
        return Path("unit")

    msg = (
        "Could not automatically determine unit tests directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'unittest_dir_name = "???"'
    )
    raise FileNotFoundError(msg)


class TOMLProjConfig(BaseModel):
    """Schema for the TOML configuration file."""

    pkg_names: list[str] | None = None
    src_rel_path: Path | None = None
    tests_rel_path: Path | None = None
    unittest_dir_name: Path | None = None
    setuptools_pkg_names: list[str] | None = None
    model_config = dict(extra="forbid")


def get_toml_config(toml_path: Path) -> TOMLProjConfig:
    """Find the configuration for a project, forced at a specific location."""
    if not toml_path.exists():
        msg = f"Could not find TOML configuration file at {toml_path}"
        raise FileNotFoundError(msg)

    with toml_path.open(mode="r") as file:
        pyproject_contents = file.read()

    if not pyproject_contents:
        msg = f"Configuration file is empty at {toml_path}"
        raise ConfigFileError(msg)

    parsed_toml: dict[str, Any] = tomllib.loads(pyproject_contents)
    config_by_tool: dict[str, Any] = parsed_toml.get("tool", {})

    try:
        config_kwargs = config_by_tool["suiteas"]
    except KeyError:
        msg = f"Could not find [tool.suiteas] configuration section at {toml_path}"
        raise ConfigFileError(msg) from None

    if not config_kwargs:
        msg = f"Empty [tool.suiteas] configuration section at {toml_path}"
        raise ConfigFileError(msg)

    try:
        setuptools_config_kwargs = config_by_tool["setuptools"]
        setuptools_pkg_names = setuptools_config_kwargs["packages"]
    except KeyError:
        setuptools_pkg_names = None

    try:
        config = TOMLProjConfig(
            **config_kwargs,
            setuptools_pkg_names=setuptools_pkg_names,
        )
    except ValidationError as err:
        msg = f"Invalid [tool.suiteas] configuration section at {toml_path}: {err}"
        raise ConfigFileError(msg) from None

    return config
