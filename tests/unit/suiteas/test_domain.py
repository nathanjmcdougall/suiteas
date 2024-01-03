from suiteas.domain import Func


class TestFunc:
    def test_is_underscored(self) -> None:
        func = Func(name="_hello", full_name="_hello", line_num=1, char_offset=1)
        assert func.is_underscored

    def test_is_not_underscored(self) -> None:
        func = Func(name="hello", full_name="hello", line_num=1, char_offset=1)
        assert not func.is_underscored
