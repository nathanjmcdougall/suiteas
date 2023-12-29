from pathlib import Path

from suiteas.config import ProjConfig
from suiteas.domain import (
    Codebase,
    File,
    Func,
    Project,
    PytestClass,
    PytestFile,
    PytestSuite,
)


class TestFunc:
    def test_is_underscored(self) -> None:
        func = Func(name="_hello")
        assert func.is_underscored

    def test_is_not_underscored(self) -> None:
        func = Func(name="hello")
        assert not func.is_underscored


class TestFile:
    def test_init(self) -> None:
        File(path=Path("example.py"), funcs=[], clses=[])


class TestCodebase:
    def test_init(self) -> None:
        Codebase(files=[])


class TestPytestClass:
    def test_init(self) -> None:
        PytestClass(name="TestClass")


class TestPytestFile:
    def test_init(self) -> None:
        PytestFile(path=Path("test_example.py"), pytest_classes=[])


class TestProject:
    def test_init(self) -> None:
        Project(
            codebase=Codebase(files=[]),
            pytest_suite=PytestSuite(pytest_files=[]),
            config=ProjConfig(pkg_names=[]),
        )
