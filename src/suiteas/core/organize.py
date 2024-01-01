"""Functionality to get the ideal testing suite structure."""

from pathlib import Path

from pydantic.alias_generators import to_pascal

from suiteas.config import ProjConfig
from suiteas.core.pytest import TEST_CLASS_PREFIX, TEST_FUNC_PREFIX
from suiteas.domain import Func, Project, PytestClass, PytestFile, PytestSuite


def _path_to_test_path(*, path: Path, proj_config: ProjConfig) -> Path:
    """Convert a path to a test path."""
    rel_path = path.relative_to(proj_config.src_rel_path)
    test_parent_path = (
        proj_config.tests_rel_path / proj_config.unittest_dir_name / rel_path.parent
    )
    test_path = test_parent_path / f"{TEST_FUNC_PREFIX}_{path.stem}.py"
    return test_path


def _func_to_test_class(func: Func) -> PytestClass:
    """Convert a function to a test class."""
    funcname = to_pascal(func.name)
    name = f"{TEST_CLASS_PREFIX}{funcname}"
    pytest_class = PytestClass(name=name)
    return pytest_class


def organize_test_suite(project: Project) -> PytestSuite:
    """Get an ideally organized test suite structure for a Python Project."""
    pytest_files = [
        PytestFile(
            path=_path_to_test_path(
                path=file.path,
                proj_config=project.config,
            ),
            pytest_classes=[_func_to_test_class(func) for func in file.funcs],
        )
        for file in project.codebase.files
    ]

    return PytestSuite(pytest_files=pytest_files)
