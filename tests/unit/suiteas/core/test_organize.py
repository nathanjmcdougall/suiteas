"""Test the `suiteas.core.organize` module."""


from typing import Self

from suiteas.core.config import PkgConfig
from suiteas.core.organize import organize_test_suite
from suiteas_test.codebase import empty_codebase, onefunc_file_codebase
from suiteas_test.test_suite import empty_test_suite, oneclass_file_testsuite


def standard_pkg_config(pkg_name: str) -> PkgConfig:
    """A standard package configuration for a single package."""
    return PkgConfig(pkg_names=[pkg_name])


class TestOrganizeTestSuite:
    """Test the `organize_test_suite` function."""

    def test_empty_codebase(self: Self, pkg_name: str) -> None:
        """Test an empty codebase."""
        codebase = empty_codebase()
        old_test_suite = empty_test_suite()
        new_test_suite = empty_test_suite()
        pkg_config = standard_pkg_config(pkg_name=pkg_name)
        assert (
            organize_test_suite(codebase, old_test_suite, pkg_config) == new_test_suite
        )

    def test_onefunc_nosuite(self: Self) -> None:
        """Test a codebase with a single file but an empty test suite."""

        pkg_config = PkgConfig(
            tests_rel_path="tests",
            src_rel_path="src",
            pkg_names=["example"],
            unittest_dir_name="unit",
        )
        codebase = onefunc_file_codebase(
            path="src/example/core/a.py",
            func_name="get_a",
        )
        old_test_suite = empty_test_suite()
        new_test_suite = oneclass_file_testsuite(
            path="tests/unit/example/core/test_a.py",
            test_class_name="TestGetA",
        )
        assert (
            organize_test_suite(codebase, old_test_suite, pkg_config) == new_test_suite
        )
