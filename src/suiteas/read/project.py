"""Utilities to reading-in a Python project."""

from pathlib import Path

from suiteas.core.path import path_to_pytest_path, pytest_path_to_path
from suiteas.domain import Project
from suiteas.read.codebase import get_codebase
from suiteas.read.config import get_config
from suiteas.read.pytest_suite import get_pytest_suite


def get_project(*, proj_dir: Path, included_files: list[Path] | None = None) -> Project:
    """Get a project from a directory."""
    if included_files is None:
        included_files = []

    config = get_config(proj_dir=proj_dir)

    included_files = [path.resolve() for path in included_files]

    if included_files:
        included_src_files = [
            proj_dir / path
            for path in included_files
            if any(
                proj_dir / config.src_rel_path / pkg_name in path.parents
                for pkg_name in config.pkg_names
            )
        ]
        if config.use_consolidated_tests_dir:
            included_pytest_files = [
                proj_dir / path
                for path in included_files
                if proj_dir / config.tests_rel_path in path.parents
            ]
        else:
            included_pytest_files = [
                proj_dir / path
                for path in included_files
                if any(
                    proj_dir
                    / config.tests_rel_path
                    / config.unittest_dir_name
                    / pkg_name
                    in path.parents
                    for pkg_name in config.pkg_names
                )
            ]
        included_src_files += [
            pytest_path_to_path(test_path, proj_config=config, proj_dir=proj_dir)
            for test_path in included_pytest_files
        ]
        included_pytest_files += [
            path_to_pytest_path(path, proj_config=config, proj_dir=proj_dir)
            for path in included_src_files
        ]
        included_src_files = list(
            {path for path in included_src_files if path.exists()},
        )
        included_pytest_files = list(
            {path for path in included_pytest_files if path.exists()},
        )
    else:
        included_src_files = None
        included_pytest_files = None

    codebase = get_codebase(
        proj_dir=proj_dir,
        config=config,
        included_src_files=included_src_files,
    )
    pytest_suite = get_pytest_suite(
        proj_dir=proj_dir,
        config=config,
        included_pytest_files=included_pytest_files,
    )

    project = Project(
        codebase=codebase,
        pytest_suite=pytest_suite,
        config=config,
        proj_dir=proj_dir,
    )
    return project
