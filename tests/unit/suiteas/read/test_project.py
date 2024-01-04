from pathlib import Path

import pytest

from suiteas.domain import (
    Codebase,
    File,
    Func,
    ProjConfig,
    Project,
    PytestFile,
    PytestSuite,
)
from suiteas.read.project import get_project


class TestGetProject:
    def test_trivial_pass(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "trivial_pass"
        project = get_project(proj_dir=proj_dir)

        expected_project = Project(
            codebase=Codebase(
                files=[
                    File(
                        path=proj_dir / "src" / "af8o7tt1" / "__init__.py",
                        funcs=[],
                        clses=[],
                        imported_objs=[],
                    ),
                ],
            ),
            pytest_suite=PytestSuite(
                pytest_files=[
                    PytestFile(
                        path=proj_dir / "tests" / "unit" / "af8o7tt1" / "__init__.py",
                        pytest_classes=[],
                        imported_objs=[],
                    ),
                ],
            ),
            config=ProjConfig(pkg_names=["af8o7tt1"]),
            proj_dir=proj_dir,
        )

        assert type(project) == Project
        assert project.model_dump() == expected_project.model_dump()

    def test_nonexistent(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            get_project(proj_dir=tmp_path)

    def test_no_tests_dir(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "no_tests_dir"

        with pytest.raises(FileNotFoundError):
            get_project(proj_dir=proj_dir)

    def test_no_unit_dir(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "no_unit_dir"
        project = get_project(proj_dir=proj_dir)
        expected_project = Project(
            codebase=Codebase(
                files=[
                    File(
                        path=proj_dir / "src" / "tx41rdni" / "__init__.py",
                        funcs=[],
                        clses=[],
                        imported_objs=[],
                    ),
                ],
            ),
            pytest_suite=PytestSuite(pytest_files=[]),
            config=ProjConfig(
                pkg_names=["tx41rdni"],
                unittest_dir_name=Path("."),
                use_consolidated_tests_dir=True,
            ),
            proj_dir=proj_dir,
        )
        assert type(project) == Project
        assert project.model_dump() == expected_project.model_dump()

    def test_one_func_no_test(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "one_func_no_test"
        project = get_project(proj_dir=proj_dir)

        expected_project = Project(
            codebase=Codebase(
                files=[
                    File(
                        path=proj_dir / "src" / "pp8cadfs" / "__init__.py",
                        funcs=[
                            Func(
                                name="hello",
                                full_name="pp8cadfs.hello",
                                line_num=1,
                                char_offset=0,
                            ),
                        ],
                        clses=[],
                        imported_objs=[],
                    ),
                ],
            ),
            pytest_suite=PytestSuite(
                pytest_files=[
                    PytestFile(
                        path=proj_dir / "tests" / "unit" / "pp8cadfs" / "__init__.py",
                        pytest_classes=[],
                        imported_objs=[],
                    ),
                ],
            ),
            config=ProjConfig(pkg_names=["pp8cadfs"]),
            proj_dir=proj_dir,
        )

        assert type(project) == Project
        assert project.model_dump() == expected_project.model_dump()
