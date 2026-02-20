"""
Parser-safe lazy loading utilities (minimal stub).

This file contains a lightweight LazyModule and helper used to restore
importability while the codebase is being repaired.
"""
from importlib import import_module
from typing import Any


class LazyModule:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: Any | None = None

    def _load(self) -> Any:
        if self._module is None:
            self._module = import_module(self._module_name)
        return self._module

    def __getattr__(self, name: str) -> Any:
        return getattr(self._load(), name)


def lazy_import(module_name: str) -> LazyModule:
    return LazyModule(module_name)


__all__ = ["LazyModule", "lazy_import"]
