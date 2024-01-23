import pytest

def test_nothing():
    assert True

@pytest.mark.parametrize("param", [True, False])
def test_param(param):
    assert param