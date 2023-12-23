"""Utilities for reading-in source code files."""
import ast
from pathlib import Path

from suiteas.domain import File, Func


def get_file(path: Path) -> File:
    """Read a file."""
    if not path.exists():
        msg = f"Could not find {path}"
        raise FileNotFoundError(msg)

    with path.open(mode="r") as file:
        source = file.read()
        tree = ast.parse(source)
        funcs = [
            Func(name=node.name)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]

    return File(path=path, funcs=funcs)
