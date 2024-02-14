from pathlib import Path

import pytest
import tomli

from suiteas.domain import ProjConfig
from suiteas.read.config import (
    ConfigFileError,
    EmptyConfigFileError,
    TOMLProjConfig,
    get_config,
    get_toml_config,
)


class TestGetConfig:
    def test_nonexistent(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            FileNotFoundError,
            match=".*Could not find configuration file nor determine the source.*",
        ):
            get_config(proj_dir=projs_parent_dir / "nonexistent")

    def test_empty_config(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=".*Could not automatically determine source directory.*",
        ):
            get_config(proj_dir=projs_parent_dir / "empty_config")

    def test_autosrc(self, projs_parent_dir: Path) -> None:
        """Test we can automatically find the source folder at src."""
        assert get_config(proj_dir=projs_parent_dir / "autosrc") == ProjConfig(
            pkg_names=[],
        )

    def test_autopkgnamesrc(self, projs_parent_dir: Path) -> None:
        """Test we can automatically find the source folder at pkg name."""
        assert get_config(proj_dir=projs_parent_dir / "autopkgnamesrc") == ProjConfig(
            pkg_names=["ixvm0b6u"],
            src_rel_path=".",
        )

    def test_autoprojnamesrc(self, projs_parent_dir: Path) -> None:
        """Test we can determine the source folder is the name of the project."""
        assert get_config(proj_dir=projs_parent_dir / "autoprojnamesrc") == ProjConfig(
            pkg_names=["pr4a7g7m"],
            src_rel_path=".",
        )

    def test_autosetuptoolssrc(self, projs_parent_dir: Path) -> None:
        """Test we can determine the source folder is the name setuptools pkg."""
        assert get_config(
            proj_dir=projs_parent_dir / "autosetuptoolssrc",
        ) == ProjConfig(
            pkg_names=["euul5ld4"],
            src_rel_path=".",
        )

    def test_automultipkgnamesrc(self, projs_parent_dir: Path) -> None:
        assert get_config(
            proj_dir=projs_parent_dir / "automultipkgnamesrc",
        ) == ProjConfig(
            pkg_names=["g5qyyvdv", "zhd1kcvi"],
            src_rel_path=".",
        )

    def test_automultisetuptoolssrc(self, projs_parent_dir: Path) -> None:
        assert get_config(
            proj_dir=projs_parent_dir / "automultisetuptoolssrc",
        ) == ProjConfig(
            pkg_names=["lh0fehzp", "z00rc6ru"],
            src_rel_path=".",
        )

    def test_autoall(self, projs_parent_dir: Path) -> None:
        """Test we can automatically determine everything without pyproject.toml."""
        assert get_config(proj_dir=projs_parent_dir / "autoall") == ProjConfig(
            pkg_names=["p8eovx9k"],
            src_rel_path=Path("src"),
            tests_rel_path=Path("tests"),
            unittest_dir_name=Path("unit"),
        )

    def test_srcconfig_only(self, projs_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=".*Could not automatically determine package names.*",
        ):
            get_config(proj_dir=projs_parent_dir / "srcconfig_only")

    def test_unitrootdir(self, projs_parent_dir: Path) -> None:
        assert get_config(proj_dir=projs_parent_dir / "unitrootdir") == ProjConfig(
            pkg_names=["wm96nwsm"],
            src_rel_path=Path("src"),
            tests_rel_path=Path("tests"),
            unittest_dir_name=Path("."),
            use_consolidated_tests_dir=True,
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
            ignore=["SUI002"],
        )

    def test_syntax_error(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(tomli.TOMLDecodeError):
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

    def test_bad_ignore(self, config_files_parent_dir: Path) -> None:
        with pytest.raises(
            ConfigFileError,
            match=(
                r"Invalid \[tool.suiteas\] configuration section at .*: "
                r"1 validation error for TOMLProjConfig\n"
                r"ignore.0\n"
                r".* Input should be .* "
                r"[type=literal_error, input_value='bad', input_type=str].*"
            ),
        ):
            get_toml_config(config_files_parent_dir / "bad_ignore.toml")
