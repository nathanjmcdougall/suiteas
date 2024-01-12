from pathlib import Path

from suiteas.domain import PytestClass, PytestFile
from suiteas.read.pytest_file import get_pytest_file


class TestGetPytestFile:
    def test_empty(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_empty.py", module_name="example",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_empty.py",
            pytest_classes=[],
            imported_objs=[],
        )
        assert pytest_file == exp_pytest_file

    def test_one_class(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_one_class.py",
            module_name="example",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_one_class.py",
            pytest_classes=[
                PytestClass(
                    name="TestMyClass",
                    has_funcs=False,
                ),
            ],
            imported_objs=[],
        )
        assert pytest_file == exp_pytest_file

    def test_one_class_one_func(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_one_class_one_func.py",
            module_name="example",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_one_class_one_func.py",
            pytest_classes=[
                PytestClass(
                    name="TestMyClass",
                    has_funcs=True,
                ),
            ],
            imported_objs=[],
        )
        assert pytest_file == exp_pytest_file

    def test_two_classes(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_two_classes.py",
            module_name="example",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_two_classes.py",
            pytest_classes=[
                PytestClass(
                    name="TestMyClass",
                    has_funcs=True,
                ),
                PytestClass(
                    name="TestMyOtherClass",
                    has_funcs=False,
                ),
            ],
            imported_objs=[],
        )
        assert pytest_file == exp_pytest_file
