"""Functionality to check whether a test suite is compliant."""


from pydantic.alias_generators import to_snake

from suiteas.core.path import path_to_test_path
from suiteas.core.pytest import TEST_CLASS_PREFIX
from suiteas.core.violations import Violation, missing_test_func
from suiteas.domain import Func, Project, PytestFile


def get_violations(project: Project) -> list[Violation]:
    """Check whether a test suite is compliant, and get a list of any violations."""

    violations = []

    pytest_file_by_rel_path = {
        pytest_file.path.relative_to(project.proj_dir): pytest_file
        for pytest_file in project.pytest_suite.pytest_files
    }

    # Check SUI001: missing-test-module
    for file in project.codebase.files:
        if not file.funcs:
            continue

        test_rel_path = path_to_test_path(
            path=file.path,
            proj_config=project.config,
            proj_dir=project.proj_dir,
        )
        pytest_file = pytest_file_by_rel_path.get(test_rel_path)

        for func in file.funcs:
            if func.is_underscored:
                continue
            if not _pytest_file_has_func_tests(pytest_file=pytest_file, func=func):
                violations.append(
                    Violation(
                        viol_cat=missing_test_func,
                        rel_path=file.path.relative_to(project.proj_dir),
                        line_num=func.line_num,
                        char_offset=func.char_offset,
                        fmt_info=dict(
                            func=func.name,
                            pytest_file_rel_posix=test_rel_path.as_posix(),
                        ),
                    ),
                )

    return violations


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
        ) == to_snake(TEST_CLASS_PREFIX) + func.name.replace("_", ""):
            return True
    return False
