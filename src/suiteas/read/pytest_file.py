"""Utilities for reading-in a pytest test file."""


from pathlib import Path

import pytest

from suiteas.core.names import PYTEST_CLASS_PREFIX, PYTEST_FUNC_PREFIX
from suiteas.domain import Class, Func, PytestClass, PytestFile, PytestFunc
from suiteas.read.file import get_file


def get_pytest_file(
    path: Path,
    *,
    module_name: str,
    pytest_items: list[pytest.Item] | None = None,
) -> PytestFile:
    """Read a pytest test file."""
    if pytest_items is None:
        pytest_items = []

    file = get_file(path, module_name=module_name)
    pytest_classes = [
        PytestClass(
            name=cls.name,
            full_name=cls.full_name,
            line_num=cls.line_num,
            char_offset=cls.char_offset,
            funcs=cls.funcs,
            pytest_funcs=[
                PytestFunc(
                    name=func.name,
                    full_name=func.full_name,
                    line_num=func.line_num,
                    char_offset=func.char_offset,
                )
                for func in cls.funcs
                if _is_pytest_func(func, pytest_items=pytest_items)
            ],
        )
        for cls in file.clses
        if _is_pytest_class(cls)
    ]
    lone_pytest_funcs = [
        PytestFunc(**func.model_dump())
        for func in file.funcs
        if _is_pytest_func(func, pytest_items=pytest_items)
    ]

    return PytestFile(
        path=file.path,
        funcs=file.funcs,
        clses=file.clses,
        imported_objs=file.imported_objs,
        lone_pytest_funcs=lone_pytest_funcs,
        pytest_clses=pytest_classes,
    )


def _is_pytest_class(cls: Class) -> bool:
    """Check if a class is a pytest class."""
    return cls.name.startswith(PYTEST_CLASS_PREFIX)


def _is_pytest_func(func: Func, *, pytest_items: list[pytest.Item]) -> bool:
    """Check if a function is a pytest function."""
    if pytest_items:
        raise NotImplementedError
    return func.name.startswith(PYTEST_FUNC_PREFIX)
