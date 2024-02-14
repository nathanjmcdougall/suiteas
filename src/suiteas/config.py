"""Configuration for the Python project to be analyzed."""

from pathlib import Path

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from suiteas.core.rules import RULE_CODES, RuleCode


class ProjConfig(BaseModel):
    """Configuration for the Python project to be analyzed."""

    pkg_names: list[str]
    src_rel_path: Path = Path("src")
    tests_rel_path: Path = Path("tests")
    unittest_dir_name: Path = Path("unit")
    use_consolidated_tests_dir: bool = False
    checks: list[RuleCode] = RULE_CODES

    @model_validator(mode="after")
    def check_consolidation_consistency(self) -> Self:
        """Check that the configuration is consistent with the consolidation setting."""
        if self.use_consolidated_tests_dir:
            if self.unittest_dir_name != Path("."):
                msg = (
                    "unittest_dir_name must be '.' when "
                    "use_consolidated_tests_dir is True"
                )
                raise ValueError(msg)
            if len(self.pkg_names) != 1:
                msg = (
                    "pkg_names must have length 1 when "
                    "use_consolidated_tests_dir is True"
                )
                raise ValueError(msg)
        return self
