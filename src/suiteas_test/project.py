"""Project instances for testing purposes."""
from suiteas.config import ProjConfig
from suiteas.domain import Project
from suiteas_test.codebase import empty_codebase
from suiteas_test.test_suite import empty_test_suite


def empty_project(pkg_name: str) -> Project:
    """A Python project with empty codebase and empty test suite."""
    codebase = empty_codebase()
    old_test_suite = empty_test_suite()
    proj_config = ProjConfig(pkg_names=[pkg_name])
    project = Project(
        codebase=codebase,
        pytest_suite=old_test_suite,
        config=proj_config,
    )
    return project
