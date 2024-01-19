from pathlib import Path

from suiteas.domain import Class, Func, PytestClass, PytestFile, PytestFunc
from suiteas.read.pytest_file import get_pytest_file


class TestGetPytestFile:
    def test_empty(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_empty.py",
            module_name="example",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_empty.py",
            funcs=[],
            clses=[],
            imported_objs=[],
            lone_pytest_funcs=[],
            pytest_clses=[],
        )
        assert pytest_file == exp_pytest_file

    def test_one_class(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_one_class.py",
            module_name="example.test_one_class",
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_one_class.py",
            funcs=[],
            clses=[
                Class(
                    name="TestMyClass",
                    full_name="example.test_one_class.TestMyClass",
                    line_num=1,
                    char_offset=0,
                    funcs=[],
                ),
            ],
            lone_pytest_funcs=[],
            pytest_clses=[
                PytestClass(
                    name="TestMyClass",
                    full_name="example.test_one_class.TestMyClass",
                    line_num=1,
                    char_offset=0,
                    funcs=[],
                    pytest_funcs=[],
                ),
            ],
            imported_objs=[],
        )
        assert pytest_file == exp_pytest_file

    def test_one_class_one_func(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_one_class_one_func.py",
            module_name="example.test_one_class_one_func",
        )
        cls = Class(
            name="TestMyClass",
            full_name="example.test_one_class_one_func.TestMyClass",
            line_num=1,
            char_offset=0,
            funcs=[
                Func(
                    name="test_my_func",
                    full_name=(
                        "example.test_one_class_one_func.TestMyClass.test_my_func"
                    ),
                    line_num=2,
                    char_offset=4,
                ),
            ],
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_one_class_one_func.py",
            funcs=[],
            clses=[cls],
            imported_objs=[],
            lone_pytest_funcs=[],
            pytest_clses=[
                PytestClass(
                    **cls.model_dump(),
                    pytest_funcs=[
                        PytestFunc(**funcs.model_dump()) for funcs in cls.funcs
                    ],
                ),
            ],
        )
        assert pytest_file == exp_pytest_file

    def test_two_classes(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_two_classes.py",
            module_name="example.test_two_classes",
        )
        cls1 = Class(
            name="TestMyClass",
            full_name="example.test_two_classes.TestMyClass",
            line_num=1,
            char_offset=0,
            funcs=[
                Func(
                    name="test_my_func",
                    full_name="example.test_two_classes.TestMyClass.test_my_func",
                    line_num=2,
                    char_offset=4,
                ),
            ],
        )
        cls2 = Class(
            name="TestMyOtherClass",
            full_name="example.test_two_classes.TestMyOtherClass",
            line_num=5,
            char_offset=0,
            funcs=[],
        )
        exp_pytest_file = PytestFile(
            path=files_parent_dir / "test_two_classes.py",
            funcs=[],
            clses=[cls1, cls2],
            imported_objs=[],
            lone_pytest_funcs=[],
            pytest_clses=[
                PytestClass(
                    **cls.model_dump(),
                    pytest_funcs=[
                        PytestFunc(**funcs.model_dump()) for funcs in cls.funcs
                    ],
                )
                for cls in [cls1, cls2]
            ],
        )
        assert pytest_file == exp_pytest_file
