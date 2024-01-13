"""A small test module."""

import pytest

class TestThings:
    """A small test class."""

    @pytest.mark.parametrize("param", [True, False])
    def test_nothing(self, param):
        assert param


@pytest.mark.parametrize("param", [True, False])
class TestParam:
    def test_nothing(self, param):
        assert param
