from pathlib import Path

import pytest
from pysource_codegen._codegen import generate

from suiteas.core.read.file import AnalyzedFileSyntaxError, get_file
from suiteas.domain import Class, File, Func
from suiteas_test.config import FAST_TESTS


class TestGetFile:
    def test_nonexistent(self, root_dir: Path) -> None:
        file_path = root_dir / "fake_mcfake_face.py"

        with pytest.raises(FileNotFoundError):
            get_file(file_path)

    def test_empty(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "empty.py"
        file = get_file(file_path)

        expected_file = File(path=file_path, funcs=[], clses=[])

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_one_func(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "one_func.py"
        file = get_file(file_path)

        expected_file = File(
            path=file_path,
            funcs=[Func(name="hello")],
            clses=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_hidden_func(self, files_parent_dir: Path) -> None:
        """A case where the function is hidden in an if-statement."""
        file_path = files_parent_dir / "nested_func.py"
        file = get_file(file_path)

        expected_file = File(
            path=file_path,
            funcs=[Func(name="make_hello")],
            clses=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_branch_logic_func(self, files_parent_dir: Path) -> None:
        """A case where the function is defined piecewise between if/for-statements."""
        file_path = files_parent_dir / "branch_logic_func.py"
        file = get_file(file_path)

        expected_file = File(
            path=file_path,
            funcs=[Func(name="hello"), Func(name="goodbye")],
            clses=[],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_invalid_syntax(self, files_parent_dir: Path) -> None:
        """A case where the file has invalid syntax."""
        file_path = files_parent_dir / "invalid_syntax.py"

        with pytest.raises(AnalyzedFileSyntaxError):
            get_file(file_path)

    def test_one_class(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "one_class.py"
        file = get_file(file_path)

        expected_file = File(
            path=file_path,
            funcs=[],
            clses=[Class(name="Banana")],
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
            file = get_file(file_path)
        except AnalyzedFileSyntaxError:
            return
        assert type(file) == File
