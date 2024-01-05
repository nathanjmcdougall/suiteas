from pathlib import Path

from suiteas.core.path import path_to_pytest_path, pytest_path_to_path
from suiteas.domain import ProjConfig


class TestPytestPathToPath:
    def test_basic(self) -> None:
        assert pytest_path_to_path(
            Path("example/subfolder/repo/tests/unit/fakemcfake/test_example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake"],
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/src/fakemcfake/example.py")


class TestPathToPytestPath:
    def test_basic(self) -> None:
        assert path_to_pytest_path(
            Path("example/subfolder/repo/src/fakemcfake/example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake"],
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/tests/unit/fakemcfake/test_example.py")
