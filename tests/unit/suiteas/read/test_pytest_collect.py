from pathlib import Path

import pytest

from suiteas.read.pytest_collect import collect_test_items


class TestCollectTestItems:
    def test_empty(self, projs_parent_dir: Path) -> None:
        assert collect_test_items(projs_parent_dir / "empty") == []

    def test_one_test(self, projs_parent_dir: Path) -> None:
        (item,) = collect_test_items(projs_parent_dir / "one_test")
        (relfspath, lineno, testname) = item.location
        assert Path(relfspath) == Path("tests/unit/cnmbqr9a/test_hello.py")
        assert lineno is not None
        assert lineno + 1 == 19
        assert testname == "TestThings.test_nothing"

    def test_paramtest(self, projs_parent_dir: Path) -> None:
        items = collect_test_items(projs_parent_dir / "paramtest")
        results = set()
        for item in items:
            (relfspath, lineno, testname) = item.location
            assert lineno is not None
            results.add((Path(relfspath), lineno + 1, testname))

        expected = {
            (
                Path("tests/unit/h10mfz3s/test_hello.py"),
                8,
                "TestThings.test_nothing[True]",
            ),
            (
                Path("tests/unit/h10mfz3s/test_hello.py"),
                8,
                "TestThings.test_nothing[False]",
            ),
            (
                Path("tests/unit/h10mfz3s/test_hello.py"),
                15,
                "TestParam.test_nothing[True]",
            ),
            (
                Path("tests/unit/h10mfz3s/test_hello.py"),
                15,
                "TestParam.test_nothing[False]",
            ),
        }

        assert results == expected

    def test_all_suppressed(self, projs_parent_dir: Path) -> None:
        assert collect_test_items(projs_parent_dir / "ignored_tests") == []

    def test_partially_suppressed(self, projs_parent_dir: Path) -> None:
        assert (
            len(collect_test_items(projs_parent_dir / "partially_ignored_tests")) == 1
        )

    def test_nonexistent(self) -> None:
        with pytest.raises(FileNotFoundError):
            collect_test_items(Path("Fakey McFake"))

    def test_nondir(self, tmp_path: Path) -> None:
        (tmp_path / "fakey").touch()
        with pytest.raises(ValueError, match="is not a directory"):
            collect_test_items(tmp_path / "fakey")

    def test_decorated(self, projs_parent_dir: Path) -> None:
        items = collect_test_items(projs_parent_dir / "decorated_test")
        assert len(items) == 3
        item1, item2, item3 = items
        assert item1.name == "test_nothing"
        assert item2.name == "test_param[True]"
        assert item3.name == "test_param[False]"

        _, lineno, _ = item2.reportinfo()
        assert lineno is not None
        assert lineno + 1 == 6  # i.e. the decorator, not the function itself.

        _, lineno, _ = item3.reportinfo()
        assert lineno is not None
        assert lineno + 1 == 6
