import tomllib
from pathlib import Path

import pytest

from suiteas.core.read.config import ConfigFileError, get_toml_config


class TestGetTOMLConfig:
    def test_nonexistent(self) -> None:
        with pytest.raises(
            FileNotFoundError,
            match="Could not find TOML configuration file at .*",
        ):
            get_toml_config(Path("fakey_mcfake_face.toml"))

    def test_empty(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(ConfigFileError, match="Configuration file is empty at .*"):
            get_toml_config(config_files_parent_dir / "empty.toml")

    def test_syntax_error(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(tomllib.TOMLDecodeError):
            get_toml_config(config_files_parent_dir / "syntax_err.toml")

    def test_no_section(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=r"Could not find \[tool.suiteas\] configuration section at .*",
        ):
            get_toml_config(config_files_parent_dir / "no_section.toml")

    def test_superfluous(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=(
                r"Invalid \[tool.suiteas\] configuration section at .*: "
                r"1 validation error for TOMLProjConfig\n"
                r"bad\n"
                r".* Extra inputs are not permitted .*"
            ),
        ):
            get_toml_config(config_files_parent_dir / "superfluous.toml")
