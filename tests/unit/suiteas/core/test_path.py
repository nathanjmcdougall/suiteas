from suiteas.core.path import path_to_pytest_path, pytest_path_to_path


class TestPytestPathToPath:
    def test_nothing(self) -> None:
        _ = pytest_path_to_path


class TestPathToPytestPath:
    def test_nothing(self) -> None:
        _ = path_to_pytest_path
