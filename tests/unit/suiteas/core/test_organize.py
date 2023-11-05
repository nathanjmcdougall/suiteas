"""Test the `suiteas.core.organize` module."""


from pathlib import Path
from typing import Self

import pytest

from suiteas.core.config import BASE_DIR, PKG_NAME, SRC_FOLDER, UNITTESTS_FOLDER
from suiteas.core.organize import organize_test_suite
from suiteas.domain.codeobj import (
    Codebase,
    File,
    Func,
    TestClass,
    TestFile,
    TestSuite,
)


def empty_codebase() -> Codebase:
    """An empty codebase."""
    return Codebase(files=[])


def empty_testsuite() -> TestSuite:
    """An empty test suite."""
    return TestSuite(test_files=[])


@pytest.fixture(scope="session", params=[empty_codebase()])
def codebase(request: pytest.FixtureRequest) -> Codebase:
    """A fixture for a codebase."""
    return request.param


class TestOrganizeTestSuite:
    """Test the `organize_test_suite` function."""

    def test_empty_codebase(self: Self) -> None:
        """Test an empty codebase."""
        codebase = empty_codebase()
        old_test_suite = empty_testsuite()
        new_test_suite = empty_testsuite()
        assert organize_test_suite(codebase, old_test_suite) == new_test_suite

    def test_single_func(self: Self) -> None:
        """Test a codebase with a single function."""
        path = Path(BASE_DIR) / SRC_FOLDER / PKG_NAME / "a.py"
        test_path = Path(BASE_DIR) / UNITTESTS_FOLDER / PKG_NAME / "test_a.py"

        func = Func(name="get_a")
        file = File(path=path, funcs=[func])
        codebase = Codebase(files=[file])
        old_test_suite = TestSuite(test_files=[])
        test_class = TestClass(name="TestGetA")
        new_test_file = TestFile(path=test_path, test_classes=[test_class])
        new_test_suite = TestSuite(test_files=[new_test_file])

        assert organize_test_suite(codebase, old_test_suite) == new_test_suite
