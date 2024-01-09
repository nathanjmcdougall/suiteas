from pathlib import Path

import pytest
from pysource_codegen._codegen import generate

from suiteas.domain import Class, File, Func
from suiteas.read.file import (
    _FLOW_CTRL,
    AnalyzedFileSyntaxError,
    FlowCtrlTree,
    get_file,
)
from suiteas_test.config import FAST_TESTS


class TestGetFile:
    def test_nonexistent(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            get_file(tmp_path / "face.py", module_name="fakey.mcfake.face")

    def test_empty(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "empty.py"
        file = get_file(file_path, module_name="fakey.mcfake.empty")

        expected_file = File(path=file_path, funcs=[], clses=[], imported_objs=[])

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_one_func(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "one_func.py"
        file = get_file(file_path, module_name="fakey.mcfake.one_func")

        expected_file = File(
            path=file_path,
            funcs=[
                Func(
                    name="hello",
                    line_num=1,
                    char_offset=0,
                    full_name="fakey.mcfake.one_func.hello",
                ),
            ],
            clses=[],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_hidden_func(self, files_parent_dir: Path) -> None:
        """A case where the function is hidden in an if-statement."""
        file_path = files_parent_dir / "nested_func.py"
        file = get_file(file_path, module_name="fakey.mcfake.nested_func")

        expected_file = File(
            path=file_path,
            funcs=[
                Func(
                    name="make_hello",
                    line_num=1,
                    char_offset=0,
                    full_name="fakey.mcfake.nested_func.make_hello",
                ),
            ],
            clses=[],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_branch_logic_func(self, files_parent_dir: Path) -> None:
        """A case where the function is defined piecewise between if/for-statements."""
        file_path = files_parent_dir / "branch_logic_func.py"
        file = get_file(file_path, module_name="fakey.mcfake.branch_logic_func")

        expected_file = File(
            path=file_path,
            funcs=[
                Func(
                    name="hello",
                    line_num=2,
                    char_offset=4,
                    full_name="fakey.mcfake.branch_logic_func.hello",
                ),
                Func(
                    name="goodbye",
                    line_num=9,
                    char_offset=4,
                    full_name="fakey.mcfake.branch_logic_func.goodbye",
                ),
            ],
            clses=[],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_invalid_syntax(self, files_parent_dir: Path) -> None:
        """A case where the file has invalid syntax."""
        file_path = files_parent_dir / "invalid_syntax.py"

        with pytest.raises(AnalyzedFileSyntaxError):
            get_file(file_path, module_name="fakey.mcfake.invalid_syntax")

    def test_one_class(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "one_class.py"
        file = get_file(file_path, module_name="fakey.mcfake.one_class")

        expected_file = File(
            path=file_path,
            funcs=[],
            clses=[
                Class(
                    name="Banana",
                    line_num=1,
                    char_offset=0,
                    full_name="fakey.mcfake.one_class.Banana",
                    has_funcs=False,
                ),
            ],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_lambda_func(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "lambda_func.py"
        file = get_file(file_path, module_name="fakey.mcfake.lambda_func")

        expected_file = File(
            path=file_path,
            funcs=[],
            clses=[],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_multi(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "multi.py"
        file = get_file(file_path, module_name="fakey.mcfake.multi")

        expected_file = File(
            path=file_path,
            funcs=[
                Func(
                    name="hello",
                    line_num=1,
                    char_offset=0,
                    full_name="fakey.mcfake.multi.hello",
                ),
                Func(
                    name="goodbye",
                    line_num=4,
                    char_offset=0,
                    full_name="fakey.mcfake.multi.goodbye",
                ),
            ],
            clses=[
                Class(
                    name="Banana",
                    line_num=7,
                    char_offset=0,
                    full_name="fakey.mcfake.multi.Banana",
                    has_funcs=False,
                ),
            ],
            imported_objs=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    @pytest.mark.skipif(FAST_TESTS, reason="Test is slow.")
    @pytest.mark.parametrize("seed", range(10))
    def test_random_file(self, tmp_path: Path, seed: int) -> None:
        """Generate a random file and check we can at least run the tool."""
        file_path = tmp_path / "random_file.py"
        with file_path.open(mode="w") as _f:
            _f.write(generate(seed=seed))
        try:
            file = get_file(file_path, module_name="random_file")
        except AnalyzedFileSyntaxError:
            return
        assert type(file) == File


class TestFlowCtrlTree:
    def test_correspondence(self) -> None:
        assert tuple(FlowCtrlTree.__args__) == _FLOW_CTRL
