"""Functionality to check whether a test suite is compliant."""

from suiteas.core.path import path_to_test_path
from suiteas.core.violations import Violation, missing_test_func
from suiteas.domain import Project


def get_violations(project: Project) -> list[Violation]:
    """Check whether a test suite is compliant, and get a list of any violations."""

    violations = []

    # Check SUI001: missing-test-module
    for file in project.codebase.files:
        if not file.funcs:
            continue

        test_path = path_to_test_path(
            path=file.path,
            proj_config=project.config,
            proj_dir=project.proj_dir,
        )
        if not test_path.exists():
            violations.append(
                Violation(
                    viol_cat=missing_test_func,
                    rel_path=file.path.relative_to(project.proj_dir),
                ),
            )

    return violations
