"""Run the suiteas command line interface."""
import sys
from collections.abc import Sequence


def _run_suiteas(argv: Sequence[str] | None) -> None:
    """Run the suiteas command line interface."""
    _ = argv


def run_suiteas(argv: Sequence[str] | None = None) -> None:
    """Run the suiteas command line interface."""

    try:
        _run_suiteas(argv)
    except KeyboardInterrupt:
        sys.exit(1)
