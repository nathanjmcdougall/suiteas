"""Utilities for reading a project's configuration."""
import tomllib
from pathlib import Path
from typing import Any

from suiteas.config import ProjConfig

TOML_NAME = "pyproject.toml"


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
