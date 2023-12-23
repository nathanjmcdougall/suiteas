from pathlib import Path

import pytest

from suiteas.core.read.file import get_file
from suiteas.domain import File, Func


class TestGetFile:
    def test_nonexistent(self, root_dir: Path) -> None:
        file_path = root_dir / "fake_mcfake_face.py"

        with pytest.raises(FileNotFoundError):
            get_file(file_path)

    def test_empty(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "empty.py"
        file = get_file(file_path)

        expected_file = File(path=file_path, funcs=[])

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()

    def test_one_func(self, files_parent_dir: Path) -> None:
        file_path = files_parent_dir / "one_func.py"
        file = get_file(file_path)

        expected_file = File(
            path=file_path,
            funcs=[Func(name="hello")],
        )

        assert type(file) == File
        assert file.model_dump() == expected_file.model_dump()
