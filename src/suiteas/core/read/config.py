"""Utilities for reading a project's configuration."""
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from suiteas.config import ProjConfig

TOML_NAME = "pyproject.toml"


class ConfigFileError(ValueError):
    """An invalid configuration file was found."""


class EmptyConfigFileError(ConfigFileError):
    """An empty configuration file was found."""


class TOMLProjConfig(BaseModel):
    """Schema for the TOML configuration file."""

    pkg_names: list[str] | None = None
    src_rel_path: Path | None = None
    tests_rel_path: Path | None = None
    unittest_dir_name: Path | None = None
    project_name: str | None = None
    setuptools_pkg_names: list[str] | None = None
    model_config = dict(extra="forbid")


def get_config(proj_dir: Path) -> ProjConfig:
    """Find the configuration for a project in the pyproject.toml file."""
    toml_path = proj_dir / TOML_NAME
    try:
        toml_config = get_toml_config(toml_path)
    except (FileNotFoundError, EmptyConfigFileError):
        toml_config = TOMLProjConfig()

    pkg_names = toml_config.pkg_names
    src_rel_path = toml_config.src_rel_path
    tests_rel_path = toml_config.tests_rel_path
    unittest_dir_name = toml_config.unittest_dir_name

    if pkg_names is None:
        pkg_names = _heuristic1_pkg_names(toml_config=toml_config)

    if src_rel_path is None:
        src_rel_path = _heuristic_src_rel_path(proj_dir=proj_dir, pkg_names=pkg_names)
    _validate_src_rel_path(src_rel_path, proj_dir=proj_dir)

    src_dir = proj_dir / src_rel_path

    if pkg_names is None:
        pkg_names = _heuristic2_pkg_names(src_dir=src_dir)
    pkg_names.sort()

    if tests_rel_path is None:
        tests_rel_path = _heuristic_tests_rel_path(proj_dir=proj_dir)
    _validate_tests_rel_path(tests_rel_path, proj_dir=proj_dir)
    tests_dir = proj_dir / tests_rel_path

    if unittest_dir_name is None:
        unittest_dir_name = _heuristic1_unittest_dir_name(
            tests_dir=tests_dir,
        )
    use_consolidated_tests_dir = _is_consolidated_tests_dir(
        pkg_names=pkg_names,
        tests_dir=tests_dir,
        unittest_dir_name=unittest_dir_name,
    )
    if unittest_dir_name is None:
        unittest_dir_name = _heuristic2_unittest_dir_name(
            use_consolidated_tests_dir=use_consolidated_tests_dir,
        )
    unittests_dir = tests_dir / unittest_dir_name
    _validate_unittest_dir_name(unittests_dir=unittests_dir)

    _validate_pkg_names(
        pkg_names,
        src_dir=src_dir,
        unittests_dir=unittests_dir,
        use_consolidated_tests_dir=use_consolidated_tests_dir,
    )

    return ProjConfig(
        pkg_names=pkg_names,
        src_rel_path=src_rel_path,
        tests_rel_path=tests_rel_path,
        unittest_dir_name=unittest_dir_name,
        use_consolidated_tests_dir=use_consolidated_tests_dir,
    )


def _heuristic_src_rel_path(*, proj_dir: Path, pkg_names: list[str] | None) -> Path:
    if (proj_dir / "src").exists():
        return Path("src")

    if pkg_names is not None:
        for pkg_name in pkg_names:
            if not (proj_dir / pkg_name).exists():
                break
            return Path(".")

    msg = (
        "Could not automatically determine source directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'src_rel_path = "???"'
    )
    raise ConfigFileError(msg)


def _heuristic1_pkg_names(*, toml_config: TOMLProjConfig) -> list[str] | None:
    if toml_config.setuptools_pkg_names is not None:
        return toml_config.setuptools_pkg_names

    if toml_config.project_name is not None:
        return [toml_config.project_name]

    return None


def _heuristic2_pkg_names(*, src_dir: Path) -> list[str]:
    package_names = [
        path.name
        for path in src_dir.iterdir()
        if path.is_dir() and path.name.isidentifier()
    ]
    if package_names:
        return package_names

    msg = (
        "Could not automatically determine package names for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'pkg_names = ["???"]'
    )
    raise ConfigFileError(msg)


def _heuristic_tests_rel_path(*, proj_dir: Path) -> Path:
    if (proj_dir / "tests").exists():
        return Path("tests")

    msg = (
        "Could not automatically determine tests directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'tests_rel_path = "???"'
    )
    raise ConfigFileError(msg)


def _heuristic1_unittest_dir_name(*, tests_dir: Path) -> Path | None:
    if (tests_dir / "unit").exists():
        return Path("unit")

    return None


def _heuristic2_unittest_dir_name(*, use_consolidated_tests_dir: bool) -> Path:
    if use_consolidated_tests_dir:
        return Path(".")

    msg = (
        "Could not automatically determine unit tests directory for project. "
        "Please manually configure this in pyproject.toml as follows:\n"
        "[tool.suiteas]\n"
        'unittest_dir_name = "???"'
    )
    raise ConfigFileError(msg)


def _is_consolidated_tests_dir(
    *,
    pkg_names: list[str],
    tests_dir: Path,
    unittest_dir_name: Path,
) -> bool:
    if len(pkg_names) == 1:
        (pkg_name,) = pkg_names
        if (unittest_dir_name is None or unittest_dir_name == Path(".")) and not (
            tests_dir / pkg_name
        ).exists():
            return True
    return False


def _validate_src_rel_path(src_rel_path: Path, *, proj_dir: Path) -> None:
    src_path = proj_dir / src_rel_path
    if not src_path.exists():
        msg = f"Could not find source directory {src_path}"
        raise FileNotFoundError(msg)


def _validate_pkg_names(
    pkg_names: list[str],
    *,
    src_dir: Path,
    unittests_dir: Path,
    use_consolidated_tests_dir: bool,
) -> None:
    if use_consolidated_tests_dir:
        return

    for pkg_name in pkg_names:
        pkg_dir = src_dir / pkg_name
        if not pkg_dir.exists():
            msg = f"Could not find package directory of {pkg_name} at {pkg_dir}"
            raise FileNotFoundError(msg)

        test_pkg_dir = unittests_dir / pkg_name
        if not test_pkg_dir.exists():
            msg = f"Could not find unit test directory of {pkg_name} at {test_pkg_dir}"
            raise FileNotFoundError(msg)


def _validate_unittest_dir_name(unittests_dir: Path) -> None:
    if not unittests_dir.exists():
        msg = f"Could not find unit tests directory {unittests_dir}"
        raise FileNotFoundError(msg)


def _validate_tests_rel_path(tests_rel_path: Path, *, proj_dir: Path) -> None:
    tests_path = proj_dir / tests_rel_path
    if not tests_path.exists():
        msg = f"Could not find tests directory {tests_path}"
        raise FileNotFoundError(msg)


def get_toml_config(toml_path: Path) -> TOMLProjConfig:
    """Find the configuration for a project, forced at a specific location."""
    if not toml_path.exists():
        msg = f"Could not find TOML configuration file at {toml_path}"
        raise FileNotFoundError(msg)

    with toml_path.open(mode="r") as file:
        pyproject_contents = file.read()

    if not pyproject_contents:
        msg = f"Configuration file is empty at {toml_path}"
        raise EmptyConfigFileError(msg)

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
        project_name = parsed_toml["project"]["name"]
    except KeyError:
        project_name = None

    try:
        setuptools_pkg_names = config_by_tool["setuptools"]["packages"]
    except KeyError:
        setuptools_pkg_names = None

    try:
        config = TOMLProjConfig(
            **config_kwargs,
            project_name=project_name,
            setuptools_pkg_names=setuptools_pkg_names,
        )
    except ValidationError as err:
        msg = f"Invalid [tool.suiteas] configuration section at {toml_path}: {err}"
        raise ConfigFileError(msg) from None

    return config
