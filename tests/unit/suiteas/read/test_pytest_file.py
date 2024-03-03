from pathlib import Path

from suiteas.domain import Class, Decorator, Func, PytestClass, PytestFile, PytestFunc
from suiteas.read.pytest_collect import collect_test_items
from suiteas.read.pytest_file import get_pytest_file


class TestGetPytestFile:
    def test_empty(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_empty.py",
            module_name="example",
            pytest_items=[],
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
            pytest_items=[],
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
            pytest_items=[],
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
                    decs=[],
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
                        PytestFunc(**funcs.model_dump(), is_collected=False)
                        for funcs in cls.funcs
                    ],
                ),
            ],
        )
        assert pytest_file == exp_pytest_file

    def test_two_classes(self, files_parent_dir: Path) -> None:
        pytest_file = get_pytest_file(
            files_parent_dir / "test_two_classes.py",
            module_name="example.test_two_classes",
            pytest_items=[],
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
                    decs=[],
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
                        PytestFunc(**funcs.model_dump(), is_collected=False)
                        for funcs in cls.funcs
                    ],
                )
                for cls in [cls1, cls2]
            ],
        )
        assert pytest_file == exp_pytest_file

    def test_ignored_tests(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "ignored_tests"
        pytest_items = collect_test_items(proj_dir)
        pytest_file = get_pytest_file(
            proj_dir / "tests" / "unit" / "kw6nn02r" / "test_hello.py",
            module_name="kw6nn02r.test_hello",
            pytest_items=pytest_items,
        )

        exp_pytest_file = PytestFile(
            path=proj_dir / "tests" / "unit" / "kw6nn02r" / "test_hello.py",
            funcs=[
                Func(
                    name="test_nothing",
                    full_name="kw6nn02r.test_hello.test_nothing",
                    line_num=3,
                    char_offset=0,
                    decs=[],
                ),
                Func(
                    name="test_param",
                    full_name="kw6nn02r.test_hello.test_param",
                    line_num=7,
                    char_offset=0,
                    decs=[Decorator(line_num=6)],
                ),
            ],
            clses=[],
            imported_objs=["pytest"],
            lone_pytest_funcs=[
                PytestFunc(
                    name="test_nothing",
                    full_name="kw6nn02r.test_hello.test_nothing",
                    line_num=3,
                    char_offset=0,
                    decs=[],
                    is_collected=False,
                ),
                PytestFunc(
                    name="test_param",
                    full_name="kw6nn02r.test_hello.test_param",
                    line_num=7,
                    char_offset=0,
                    decs=[Decorator(line_num=6)],
                    is_collected=False,
                ),
            ],
            pytest_clses=[],
        )
        assert pytest_file == exp_pytest_file

    def test_collected_tests(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "collected_tests"
        pytest_items = collect_test_items(proj_dir)
        pytest_file = get_pytest_file(
            proj_dir / "tests" / "unit" / "z0foz1cj" / "test_hello.py",
            module_name="z0foz1cj.test_hello",
            pytest_items=pytest_items,
        )

        exp_pytest_file = PytestFile(
            path=proj_dir / "tests" / "unit" / "z0foz1cj" / "test_hello.py",
            funcs=[
                Func(
                    name="test_nothing",
                    full_name="z0foz1cj.test_hello.test_nothing",
                    line_num=3,
                    char_offset=0,
                    decs=[],
                ),
                Func(
                    name="test_param",
                    full_name="z0foz1cj.test_hello.test_param",
                    line_num=7,
                    char_offset=0,
                    decs=[Decorator(line_num=6)],
                ),
            ],
            clses=[],
            imported_objs=["pytest"],
            lone_pytest_funcs=[
                PytestFunc(
                    name="test_nothing",
                    full_name="z0foz1cj.test_hello.test_nothing",
                    line_num=3,
                    char_offset=0,
                    decs=[],
                    is_collected=True,
                ),
                PytestFunc(
                    name="test_param",
                    full_name="z0foz1cj.test_hello.test_param",
                    line_num=7,
                    char_offset=0,
                    decs=[Decorator(line_num=6)],
                    is_collected=True,
                ),
            ],
            pytest_clses=[],
        )
        assert pytest_file == exp_pytest_file
