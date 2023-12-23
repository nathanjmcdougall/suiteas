from pathlib import Path

import pytest

from suiteas.core.run import get_project, run_suiteas_main
from suiteas.domain import (
    Codebase,
    File,
    Func,
    ProjConfig,
    Project,
    PytestFile,
    PytestSuite,
)


class TestGetProject:
    def test_trivial_pass(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "trivial_pass"
        project = get_project(proj_dir)

        expected_project = Project(
            codebase=Codebase(
                files=[
                    File(path=proj_dir / "src" / "af8o7tt1" / "__init__.py", funcs=[]),
                ],
            ),
            pytest_suite=PytestSuite(
                pytest_files=[
                    PytestFile(
                        path=proj_dir / "tests" / "unit" / "af8o7tt1" / "__init__.py",
                        pytest_classes=[],
                    ),
                ],
            ),
            config=ProjConfig(pkg_names=["af8o7tt1"]),
        )

        assert type(project) == Project
        assert project.model_dump() == expected_project.model_dump()

    def test_nonexistent(self, root_dir: Path) -> None:
        proj_dir = root_dir / "Fakey McFake Face"

        with pytest.raises(FileNotFoundError):
            get_project(proj_dir)

    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "no_tests_dir"

        with pytest.raises(FileNotFoundError):
            get_project(proj_dir)

    def test_no_unit_dir(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "no_unit_dir"

        with pytest.raises(FileNotFoundError):
            get_project(proj_dir)

    def test_one_func_no_test(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "one_func_no_test"
        project = get_project(proj_dir)

        expected_project = Project(
            codebase=Codebase(
                files=[
                    File(
                        path=proj_dir / "src" / "pp8cadfs" / "__init__.py",
                        funcs=[Func(name="hello")],
                    ),
                ],
            ),
            pytest_suite=PytestSuite(
                pytest_files=[
                    PytestFile(
                        path=proj_dir / "tests" / "unit" / "pp8cadfs" / "__init__.py",
                        pytest_classes=[],
                    ),
                ],
            ),
            config=ProjConfig(pkg_names=["pp8cadfs"]),
        )

        assert type(project) == Project
        assert project.model_dump() == expected_project.model_dump()


class TestRunSuiteMain:
    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        with pytest.raises(FileNotFoundError):
            run_suiteas_main([(projs_parent_dir / "no_tests_dir").as_posix()])
