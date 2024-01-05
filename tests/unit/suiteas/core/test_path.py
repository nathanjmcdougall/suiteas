from pathlib import Path

import pytest

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

    def test_custom_dirs(self) -> None:
        assert pytest_path_to_path(
            Path("example/subfolder/repo/mytests/myunit/fakemcfake/test_example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake", "other_package"],
                src_rel_path=Path("mysrc"),
                tests_rel_path=Path("mytests"),
                unittest_dir_name=Path("myunit"),
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/mysrc/fakemcfake/example.py")

    def test_consolidated(self) -> None:
        assert pytest_path_to_path(
            Path("example/subfolder/repo/tests/submodule/test_example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake"],
                unittest_dir_name=Path("."),
                use_consolidated_tests_dir=True,
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/src/fakemcfake/submodule/example.py")

    def test_err(self) -> None:
        with pytest.raises(ValueError, match=".* is not in the subpath of .*"):
            pytest_path_to_path(
                Path("example/subfolder/repo/tests/unit/fakemcfake/test_example.py"),
                proj_config=ProjConfig(
                    pkg_names=["fakemcfake"],
                ),
                proj_dir=Path("example/subfolder/otherrepo"),
            )


class TestPathToPytestPath:
    def test_basic(self) -> None:
        assert path_to_pytest_path(
            Path("example/subfolder/repo/src/fakemcfake/example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake"],
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/tests/unit/fakemcfake/test_example.py")

    def test_custom_dirs(self) -> None:
        assert path_to_pytest_path(
            Path("example/subfolder/repo/mysrc/fakemcfake/example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake", "other_package"],
                src_rel_path=Path("mysrc"),
                tests_rel_path=Path("mytests"),
                unittest_dir_name=Path("myunit"),
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/mytests/myunit/fakemcfake/test_example.py")

    def test_consolidated(self) -> None:
        assert path_to_pytest_path(
            Path("example/subfolder/repo/src/fakemcfake/submodule/example.py"),
            proj_config=ProjConfig(
                pkg_names=["fakemcfake"],
                unittest_dir_name=Path("."),
                use_consolidated_tests_dir=True,
            ),
            proj_dir=Path("example/subfolder/repo"),
        ) == Path("example/subfolder/repo/tests/submodule/test_example.py")

    def test_err(self) -> None:
        with pytest.raises(ValueError, match=".* is not in the subpath of .*"):
            path_to_pytest_path(
                Path("example/subfolder/repo/src/fakemcfake/example.py"),
                proj_config=ProjConfig(
                    pkg_names=["fakemcfake"],
                ),
                proj_dir=Path("example/subfolder/otherrepo"),
            )
