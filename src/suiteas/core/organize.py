"""Core organization functionality."""
from pathlib import Path

from suiteas.core.config import BASE_DIR, PKG_NAME, SRC_FOLDER, UNITTESTS_FOLDER
from suiteas.domain.codeobj import Codebase, Func, TestClass, TestFile, TestSuite


def _path_to_test_path(path: Path) -> Path:
    """Convert a path to a test path."""
    base_dir = Path(BASE_DIR)
    rel_path = path.relative_to(base_dir / SRC_FOLDER / PKG_NAME)
    test_parent_path = base_dir / UNITTESTS_FOLDER / PKG_NAME / rel_path.parent
    return test_parent_path / ("test_" + path.stem + ".py")


def _snake_case_to_camel_case(snake_case: str) -> str:
    """Convert a snake case string to a camel case string."""
    return "".join(word.capitalize() for word in snake_case.split("_"))


def _func_to_test_class(func: Func) -> TestClass:
    """Convert a function to a test class."""
    return TestClass(
        name="Test" + _snake_case_to_camel_case(func.name),
    )


def organize_test_suite(codebase: Codebase, test_suite: TestSuite) -> TestSuite:
    """Organize a codebase into a corresponding test suite."""
    _ = test_suite
    test_files = [
        TestFile(
            path=_path_to_test_path(file.path),
            test_classes=[_func_to_test_class(func) for func in file.funcs],
        )
        for file in codebase.files
    ]

    return TestSuite(test_files=test_files)
