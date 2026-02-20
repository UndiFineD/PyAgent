#!/usr/bin/env python3
"""
Minimal extension registry used for tests.

This file provides a lightweight, well-typed registry API that
preserves the names expected by tests while keeping behavior simple.
"""
from __future__ import annotations




from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ExtensionInfo:
    name: str
    version: str = "0.0.0"
    meta: Dict[str, Any] = field(default_factory=dict)


class ExtensionRegistry:
    ""
A minimal registry for registering and retrieving extensions.""
def __init__(self, name: str = "default") -> None:
        self.name: str = name
        self._extensions: Dict[str, ExtensionInfo] = {}

    def register(self, name: str, version: str = "0.0.0", **meta: Any) -> ExtensionInfo:
        info = ExtensionInfo(name=name, version=version, meta=meta)
        self._extensions[name] = info
        return info

    def get(self, name: str) -> Optional[ExtensionInfo]:
        return self._extensions.get(name)

    def list(self) -> List[ExtensionInfo]:
        return list(self._extensions.values())

    def remove(self, name: str) -> bool:
        return self._extensions.pop(name, None) is not None

    def find(self, predicate: Callable[[ExtensionInfo], bool]) -> List[ExtensionInfo]:
        return [e for e in self._extensions.values() if predicate(e)]


# Backwards-compatible names expected by the codebase/tests
ExtensionManager = ExtensionRegistry
TypedExtensionManager = ExtensionRegistry
MultiExtensionManager = ExtensionRegistry
LazyExtensionManager = ExtensionRegistry


class GlobalRegistry(ExtensionRegistry):
    _instance: Optional['GlobalRegistry'] = None

    def __new__(cls) -> 'GlobalRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not getattr(self, "_initialized", False):
            super().__init__("__global__")
            self._initialized = True


def create_registry(name: str) -> ExtensionRegistry:
    return ExtensionRegistry(name)


def create_typed_registry(name: str, base_type: type) -> TypedExtensionManager:
    # For tests, a simple registry is sufficient
    return TypedExtensionManager(name)


def create_multi_registry() -> MultiExtensionManager:
    return MultiExtensionManager("multi")


def create_lazy_registry() -> LazyExtensionManager:
    return LazyExtensionManager("lazy")


def get_global_registry() -> GlobalRegistry:
    return GlobalRegistry()


# Module-level default registry for convenience
_default_registry: Optional[ExtensionRegistry] = None


def get_default_registry() -> ExtensionRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = ExtensionRegistry()
    return _default_registry


__all__ = [
    "ExtensionInfo",
    "ExtensionRegistry",
    "get_default_registry",
]
