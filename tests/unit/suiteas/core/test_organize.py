"""Test the `suiteas.core.organize` module."""


from pathlib import Path
from typing import Self

from suiteas.core.config import PkgConfig
from suiteas.core.organize import organize_test_suite
from suiteas.domain.codeobj import (
    Codebase,
    File,
    Func,
    TestClass,
    TestFile,
    TestSuite,
)


def null_file(path: Path) -> File:
    """A file with no functions at the given path."""
    return File(path=path, funcs=[])


def onefunc_file(path: Path, func_name: str) -> File:
    """A file with a single function at the given path."""
    func = Func(name=func_name)
    return File(path=path, funcs=[func])


def empty_codebase() -> Codebase:
    """An empty codebase."""
    return Codebase(files=[])


def null_file_codebase(path: Path) -> Codebase:
    """A codebase with a single file (at the given path) with no functions."""
    return Codebase(files=[null_file(path=path)])


def onefunc_file_codebase(path: Path, func_name: str) -> Codebase:
    """A codebase with a single file (at the given path) with a single function."""
    return Codebase(files=[onefunc_file(path=path, func_name=func_name)])


def empty_testsuite() -> TestSuite:
    """An empty test suite."""
    return TestSuite(test_files=[])


def null_file_testsuite(path: Path) -> TestSuite:
    """A test suite with a single file (at the given path) with no test classes."""
    return TestSuite(test_files=[TestFile(path=path, test_classes=[])])


def onetestcls_file_testsuite(path: Path, test_class_name: str) -> TestSuite:
    """A test suite with a single file (at the given path) with a single test class."""
    test_class = TestClass(name=test_class_name)
    return TestSuite(test_files=[TestFile(path=path, test_classes=[test_class])])


def standard_pkg_config(pkg_name: str) -> PkgConfig:
    """A standard package configuration for a single package."""
    return PkgConfig(
        tests_rel_path="tests",
        src_rel_path="src",
        pkg_names=[pkg_name],
    )


class TestOrganizeTestSuite:
    """Test the `organize_test_suite` function."""

    def test_empty_codebase(self: Self) -> None:
        """Test an empty codebase."""
        codebase = empty_codebase()
        old_test_suite = empty_testsuite()
        new_test_suite = empty_testsuite()
        pkg_config = standard_pkg_config(pkg_name="example")
        assert (
            organize_test_suite(codebase, old_test_suite, pkg_config) == new_test_suite
        )

    def test_onefunc_nosuite(self: Self) -> None:
        """Test a codebase with a single file but an empty test suite."""

        pkg_config = PkgConfig(
            tests_rel_path="tests",
            src_rel_path="src",
            pkg_names=["example"],
        )
        codebase = onefunc_file_codebase(
            path="src/example/core/a.py",
            func_name="get_a",
        )
        old_test_suite = empty_testsuite()
        new_test_suite = onetestcls_file_testsuite(
            path="tests/unit/example/core/test_a.py",
            test_class_name="TestGetA",
        )
        assert (
            organize_test_suite(codebase, old_test_suite, pkg_config) == new_test_suite
        )
