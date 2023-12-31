import tomllib
from pathlib import Path

import pytest

from suiteas.core.read.config import ConfigFileError, TOMLProjConfig, get_toml_config


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

    def test_extra_subsection(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=(
                r"Invalid \[tool.suiteas\] configuration section at .*: "
                r"1 validation error for TOMLProjConfig\n"
                r"mysubsection\n"
                r".* Extra inputs are not permitted .*"
            ),
        ):
            get_toml_config(config_files_parent_dir / "extra_subsection.toml")

    def test_complete(self, config_files_parent_dir: Path) -> None:
        config = get_toml_config(config_files_parent_dir / "complete.toml")

        assert config == TOMLProjConfig(
            pkg_names=["foo", "bar"],
            src_rel_path=Path("mysrc"),
            tests_rel_path=Path("mytests"),
            unittest_dir_name=Path("myunit"),
            setuptools_pkg_names=["foo_other", "bar_other"],
        )
