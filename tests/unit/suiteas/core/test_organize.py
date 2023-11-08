"""Test the `suiteas.core.organize` module."""


from typing import Self

from suiteas.config import ProjConfig
from suiteas.core.organize import organize_test_suite
from suiteas.domain import Project
from suiteas_test.codebase import onefunc_file_codebase
from suiteas_test.project import empty_project
from suiteas_test.test_suite import empty_test_suite, oneclass_file_testsuite


class TestOrganizeTestSuite:
    def test_empty_project(self: Self, pkg_name: str) -> None:
        """Test an empty codebase."""
        assert (
            organize_test_suite(empty_project(pkg_name=pkg_name)) == empty_test_suite()
        )

    def test_onefunc_nosuite(self: Self) -> None:
        """Test a codebase with a single file but an empty test suite."""

        proj_config = ProjConfig(
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
        project = Project(
            codebase=codebase,
            pytest_suite=old_test_suite,
            config=proj_config,
        )
        assert organize_test_suite(project) == new_test_suite
