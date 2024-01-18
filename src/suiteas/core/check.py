"""Functionality to check whether a test suite is compliant."""


from pathlib import Path

from pydantic.alias_generators import to_snake

from suiteas.core.names import PYTEST_CLASS_PREFIX
from suiteas.core.path import path_to_pytest_path
from suiteas.core.rules import (
    empty_pytest_class,
    missing_test_func,
    unimported_tested_func,
)
from suiteas.core.violations import Violation
from suiteas.domain import File, Func, Project, PytestFile


def get_violations(project: Project) -> list[Violation]:
    """Check whether a test suite is compliant, and get a list of any violations."""

    violations = []

    pytest_file_by_rel_path = {
        pytest_file.path.relative_to(project.proj_dir): pytest_file
        for pytest_file in project.pytest_suite.pytest_files
    }

    for file in project.codebase.files:
        if not file.funcs:
            continue

        pytest_rel_path = path_to_pytest_path(
            path=file.path,
            proj_config=project.config,
            proj_dir=project.proj_dir,
        ).relative_to(project.proj_dir)
        pytest_file = pytest_file_by_rel_path.get(pytest_rel_path)

        for func in file.funcs:
            if func.is_underscored:
                continue

            if "SUI001" in project.config.checks:
                violations.extend(
                    _get_sui001_violations(
                        pytest_file=pytest_file,
                        func=func,
                        file=file,
                        project=project,
                        pytest_rel_path=pytest_rel_path,
                    ),
                )

            if "SUI003" in project.config.checks:
                violations.extend(
                    _get_sui003_violations(
                        pytest_file=pytest_file,
                        func=func,
                        file=file,
                        project=project,
                        pytest_rel_path=pytest_rel_path,
                    ),
                )

    # Check SUI002: empty-pytest-class
    if "SUI002" in project.config.checks:
        violations.extend(_get_sui002_violations(project=project))

    return violations


def _get_sui001_violations(
    *,
    pytest_file: PytestFile | None,
    func: Func,
    file: File,
    project: Project,
    pytest_rel_path: Path,
) -> list[Violation]:
    if not _pytest_file_has_func_tests(
        pytest_file=pytest_file,
        func=func,
    ):
        return [
            Violation(
                rule=missing_test_func,
                rel_path=file.path.relative_to(project.proj_dir),
                line_num=func.line_num,
                char_offset=func.char_offset,
                fmt_info=dict(
                    func=func.name,
                    pytest_file_rel_posix=pytest_rel_path.as_posix(),
                ),
            ),
        ]
    return []


def _get_sui002_violations(
    *,
    project: Project,
) -> list[Violation]:
    violations = []
    for pytest_file in project.pytest_suite.pytest_files:
        for pytest_class in pytest_file.pytest_classes:
            if not pytest_class.has_funcs:
                violations.append(
                    Violation(
                        rule=empty_pytest_class,
                        rel_path=pytest_file.path.relative_to(project.proj_dir),
                        fmt_info=dict(pytest_class_name=pytest_class.name),
                    ),
                )
    return violations


def _get_sui003_violations(
    *,
    pytest_file: PytestFile | None,
    func: Func,
    file: File,
    project: Project,
    pytest_rel_path: Path,
) -> list[Violation]:
    if not _pytest_file_imports_func(
        pytest_file=pytest_file,
        func=func,
    ):
        return [
            Violation(
                rule=unimported_tested_func,
                rel_path=file.path.relative_to(project.proj_dir),
                line_num=func.line_num,
                char_offset=func.char_offset,
                fmt_info=dict(
                    func_fullname=func.full_name,
                    pytest_file_rel_posix=pytest_rel_path.as_posix(),
                ),
            ),
        ]
    return []


def _pytest_file_has_func_tests(
    *,
    pytest_file: PytestFile | None,
    func: Func,
) -> bool:
    """Check whether a pytest file has tests for a function."""
    if pytest_file is None:
        return False

    for pytest_class in pytest_file.pytest_classes:
        if to_snake(pytest_class.name).replace(
            "_",
            "",
        ) == to_snake(PYTEST_CLASS_PREFIX) + func.name.replace("_", ""):
            return True
    return False


def _pytest_file_imports_func(
    *,
    pytest_file: PytestFile | None,
    func: Func,
) -> bool:
    """Check whether a pytest file imports a function."""
    if pytest_file is None:
        return True  # Tautologically

    return func.full_name in pytest_file.imported_objs
