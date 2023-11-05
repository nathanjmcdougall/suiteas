"""Test the `suiteas.core.organize` module."""

from typing import Self

from suiteas.core.organize import organize_test_suite
from suiteas.domain.codeobj import Codebase, TestSuite


class TestOrganizeTestSuite:
    """Test the `organize_test_suite` function."""

    def test_empty_codebase(self: Self) -> None:
        """Test an empty codebase."""
        codebase = Codebase(files=[])
        test_suite = TestSuite(files=[])
        assert organize_test_suite(codebase, test_suite) == test_suite
