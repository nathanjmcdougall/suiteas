"""Utilities for reading-in source code files."""
import ast
import sys
from pathlib import Path
from typing import TypeAlias

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
    ast.Global,
    ast.Nonlocal,
    ast.Expr,
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.Match,
    ast.Lambda,
)
_IMPORT = (
    ast.Import,
    ast.ImportFrom,
)
if sys.version_info < (3, 12):
    _TYPING = (ast.AnnAssign,)
else:
    _TYPING = (ast.AnnAssign, ast.TypeAlias)

_EXPR = (ast.expr, ast.Expr)
if sys.version_info < (3, 11):
    _FLOW_CTRL = (
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.If,
        ast.With,
        ast.AsyncWith,
        ast.Try,
    )
else:
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
if sys.version_info < (3, 11):
    FlowCtrlTree: TypeAlias = (
        ast.For | ast.AsyncFor | ast.While | ast.If | ast.With | ast.AsyncWith | ast.Try
    )
else:
    FlowCtrlTree: TypeAlias = (
        ast.For
        | ast.AsyncFor
        | ast.While
        | ast.If
        | ast.With
        | ast.AsyncWith
        | ast.Try
        | ast.TryStar
    )


def get_file(path: Path, *, module_name: str) -> File:
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
        funcs, clses, imported_objs = _parse_tree(tree, module_name=module_name)

    return File(path=path, funcs=funcs, clses=clses, imported_objs=imported_objs)


def _parse_tree(  # noqa: PLR0912, C901
    tree: ast.Module | FlowCtrlTree,
    *,
    module_name: str,
) -> tuple[list[Func], list[Class], list[str]]:
    """Get a File object from an ast tree."""
    funcs = []
    clses = []
    imported_objs = []

    for node in tree.body:
        if isinstance(node, _FLOW_CTRL):
            subfuncs, subclses, subimported_objs = _parse_tree(
                node,
                module_name=module_name,
            )
            funcs.extend(subfuncs)
            clses.extend(subclses)
            imported_objs.extend(subimported_objs)
        elif isinstance(node, _FUNC_DEF):
            funcs.append(
                Func(
                    name=node.name,
                    full_name=f"{module_name}.{node.name}",
                    line_num=node.lineno,
                    char_offset=node.col_offset,
                ),
            )
        elif isinstance(node, _CLS_DEF):
            has_funcs = any(isinstance(n, _FUNC_DEF) for n in node.body)
            clses.append(
                Class(
                    name=node.name,
                    full_name=f"{module_name}.{node.name}",
                    line_num=node.lineno,
                    char_offset=node.col_offset,
                    has_funcs=has_funcs,
                ),
            )
        elif isinstance(node, _IMPORT):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_objs.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_objs.append(f"{node.module}.{alias.name}")
            else:
                raise AssertionError  # noqa: TRY004

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

    return funcs, clses, imported_objs
