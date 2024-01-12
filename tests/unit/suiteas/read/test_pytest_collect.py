from suiteas.read.pytest_collect import collect_test_items


class TestCollectTestItems:
    def test_nothing(self) -> None:
        _ = collect_test_items
