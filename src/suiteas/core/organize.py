"""Core organization functionality."""
from pathlib import Path

from pydantic.alias_generators import to_pascal

from suiteas.core.config import PkgConfig
from suiteas.domain.codeobj import Codebase, Func, TestClass, TestFile, TestSuite

TEST_FUNC_PREFIX = "test_"
TEST_CLASS_PREFIX = "Test"


def _path_to_test_path(path: Path, pkg_config: PkgConfig) -> Path:
    """Convert a path to a test path."""
    rel_path = path.relative_to(pkg_config.src_rel_path)
    test_parent_path = (
        pkg_config.tests_rel_path / pkg_config.unittest_dir_name / rel_path.parent
    )
    test_path = test_parent_path / f"{TEST_FUNC_PREFIX}{path.stem}.py"
    return test_path


def _func_to_test_class(func: Func) -> TestClass:
    """Convert a function to a test class."""
    funcname = to_pascal(func.name)
    name = f"{TEST_CLASS_PREFIX}{funcname}"
    test_class = TestClass(name=name)
    return test_class


def organize_test_suite(
    codebase: Codebase,
    test_suite: TestSuite,
    pkg_config: PkgConfig,
) -> TestSuite:
    """Organize a codebase into a corresponding test suite."""
    _ = test_suite
    test_files = [
        TestFile(
            path=_path_to_test_path(file.path, pkg_config),
            test_classes=[_func_to_test_class(func) for func in file.funcs],
        )
        for file in codebase.files
    ]

    return TestSuite(test_files=test_files)
