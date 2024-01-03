"""Utilities for reading-in source code files."""
import ast
from pathlib import Path
from typing import Union

from suiteas.domain import Class, File, Func

TEST_EXPR = False


class AnalyzedFileSyntaxError(SyntaxError):
    """Raised when the file being analyzed has a syntax error."""


_FUNC_DEF = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
)
_CLS_DEF = (ast.ClassDef,)
_STMT = (
    ast.Return,
    ast.Delete,
    ast.Assign,
    ast.AugAssign,
    ast.Raise,
    ast.Assert,
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
    ast.Expr,
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.Match,
    ast.Lambda,
)
_TYPING = (ast.AnnAssign,)
_EXPR = (ast.expr, ast.Expr)
_FLOW_CTRL = (
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.If,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.TryStar,
)


def get_file(path: Path) -> File:
    """Read a file."""
    if not path.exists():
        msg = f"Could not find {path}"
        raise FileNotFoundError(msg)

    with path.open(mode="r") as _f:
        source = _f.read()
        try:
            tree = ast.parse(source)
        except SyntaxError as err:
            msg = f"Syntax error in {path}: {err}"
            raise AnalyzedFileSyntaxError(msg) from None
        funcs, clses = _get_funcs_clses_from_tree(tree)

    return File(path=path, funcs=funcs, clses=clses)


def _get_funcs_clses_from_tree(
    tree: ast.Module | Union[_FLOW_CTRL],  # noqa: UP007 since Union[(x,y)] is OK
) -> tuple[list[Func], list[Class]]:
    """Get a File object from an ast tree."""
    funcs = []
    clses = []

    for node in tree.body:
        if isinstance(node, _FLOW_CTRL):
            subfuncs, subclses = _get_funcs_clses_from_tree(node)
            funcs.extend(subfuncs)
            clses.extend(subclses)
        elif isinstance(node, _FUNC_DEF):
            funcs.append(
                Func(name=node.name, line_num=node.lineno, char_offset=node.col_offset),
            )
        elif isinstance(node, _CLS_DEF):
            clses.append(
                Class(
                    name=node.name,
                    line_num=node.lineno,
                    char_offset=node.col_offset,
                ),
            )
        elif isinstance(node, _STMT + _TYPING):
            pass
        elif isinstance(node, _EXPR):
            if TEST_EXPR:
                msg = "Testing constant values (i.e. expressions) is not yet supported."
                raise NotImplementedError(msg)
        else:
            msg = f"AST element type {type(node)} not supported."
            assert not isinstance(node, _FLOW_CTRL)
            raise NotImplementedError(msg)

    return funcs, clses
