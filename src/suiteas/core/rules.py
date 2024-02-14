"""Utilities for defining the linting rules."""


import typing
from typing import Literal, TypeAlias

from pydantic import BaseModel

RuleCode: TypeAlias = Literal["SUI001", "SUI002", "SUI003"]

RULE_CODES: list[RuleCode] = list(typing.get_args(RuleCode))


class Rule(BaseModel):
    """A rule enforced by SuiteAs."""

    rule_code: RuleCode
    name: str
    description: str


missing_test_func = Rule(
    rule_code="SUI001",
    name="missing-test-func",
    description="{func} untested in {pytest_file_rel_posix}",
)

empty_pytest_class = Rule(
    rule_code="SUI002",
    name="empty-pytest-class",
    description="{pytest_class_name} has no tests",
)

unimported_tested_func = Rule(
    rule_code="SUI003",
    name="unimported-tested-func",
    description="{func_fullname} is not imported in {pytest_file_rel_posix}",
)
