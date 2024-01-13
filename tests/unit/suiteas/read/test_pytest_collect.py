from pathlib import Path

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
