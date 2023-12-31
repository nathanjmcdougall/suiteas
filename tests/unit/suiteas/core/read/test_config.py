import tomllib
from pathlib import Path

import pytest

from suiteas.core.read.config import (
    ConfigFileError,
    EmptyConfigFileError,
    TOMLProjConfig,
    get_config,
    get_toml_config,
)


class TestGetTOMLConfig:
    def test_nonexistent(self) -> None:
        with pytest.raises(
            FileNotFoundError,
            match="Could not find TOML configuration file at .*",
        ):
            get_toml_config(Path("fakey_mcfake_face.toml"))

    def test_empty(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(EmptyConfigFileError):
            get_toml_config(config_files_parent_dir / "empty.toml")

    def test_complete(self, config_files_parent_dir: Path) -> None:
        config = get_toml_config(config_files_parent_dir / "complete.toml")

        assert config == TOMLProjConfig(
            pkg_names=["foo", "bar"],
            src_rel_path=Path("mysrc"),
            tests_rel_path=Path("mytests"),
            unittest_dir_name=Path("myunit"),
            setuptools_pkg_names=["foo_other", "bar_other"],
            project_name="example",
        )

    def test_syntax_error(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(tomllib.TOMLDecodeError):
            get_toml_config(config_files_parent_dir / "syntax_err.toml")

    def test_lists(self, config_files_parent_dir: Path) -> None:
        """Test where we use singleton lists instead of constants."""
        with pytest.raises(
            ConfigFileError,
            match=".*Input is not a valid path .* input_type=list.*",
        ):
            get_toml_config(config_files_parent_dir / "badlists.toml")

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


class TestGetConfig:
    def test_nonexistent(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=".*Could not automatically determine source directory.*",
        ):
            get_config(projs_parent_dir / "nonexistent")

    def test_empty_config(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=".*Could not automatically determine source directory.*",
        ):
            get_config(projs_parent_dir / "empty_config")

    def test_autosrc(self, projs_parent_dir: Path) -> None:
        """Test we can automatically find the source folder at src."""
        get_config(projs_parent_dir / "autosrc")

    def test_autonamesrc(self, projs_parent_dir: Path) -> None:
        """Test we can determine the source folder is the name of the project."""
        get_config(projs_parent_dir / "autonamesrc")

    def test_allauto(self, projs_parent_dir: Path) -> None:
        """Test we can automatically determine everything without pyproject.toml."""
        raise NotImplementedError

    def test_srcconfig_only(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=".*Could not automatically determine package names.*",
        ):
            get_config(projs_parent_dir / "srcconfig_only")
