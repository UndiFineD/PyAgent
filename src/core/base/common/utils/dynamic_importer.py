"""Lightweight dynamic importer utilities (minimal, repair-friendly).

This module implements small, dependency-minimal helpers used by tests
and other lightweight code paths. Implementations are intentionally
conservative to prevent cascading import failures during repair passes.
"""
from __future__ import annotations

from importlib import import_module, reload
from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType, SimpleNamespace
from typing import Any, Dict, Optional, Tuple
import sys


def import_from_path(path: str, name: Optional[str] = None) -> ModuleType:
    """Import a module from a file path in a conservative way."""
    if name is None:
        name = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from path: {path}")
    mod = module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def import_from_module(module_path: str) -> ModuleType:
    """Import by dotted module path."""
    return import_module(module_path)


def reload_module(module: ModuleType) -> ModuleType:
    """Reload a module; accepts module object or name."""
    if isinstance(module, str):
        module = import_module(module)
    return reload(module)


def unload_module(module_name: str) -> None:
    """Safely remove a module from sys.modules if present."""
    sys.modules.pop(module_name, None)


def get_module_version(module_name: str) -> Optional[str]:
    """Return installed distribution version if available, else None."""
    try:
        import importlib.metadata as metadata

        return metadata.version(module_name)
    except Exception:
        return None


def compare_versions(a: Optional[str], b: Optional[str]) -> int:
    """Compare two version strings simply: -1,0,1."""
    if not a or not b:
        return 0
    try:
        from packaging.version import Version

        va, vb = Version(a), Version(b)
        if va < vb:
            return -1
        if va > vb:
            return 1
        return 0
    except Exception:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0


def ensure_module(module_name: str) -> Tuple[bool, Optional[str]]:
    """Return (available, version) for a module name."""
    try:
        mod = import_module(module_name)
        version = getattr(mod, "__version__", None)
        if not version:
            version = get_module_version(module_name)
        return True, version
    except Exception:
        return False, None


class PlaceholderModule(SimpleNamespace):
    """Tiny placeholder for absent modules during tests."""


class LazyAttribute:
    """Descriptor-style helper representing a lazily resolved attribute."""

    def __init__(self, module_name: str, attr_name: str):
        self.module_name = module_name
        self.attr_name = attr_name

    def resolve(self) -> Any:
        mod = import_module(self.module_name)
        return getattr(mod, self.attr_name)


class LazyModuleRegistry:
    """Very small registry for lazily registered modules."""

    def __init__(self):
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, module: Any) -> None:
        self._registry[name] = module

    def get(self, name: str) -> Any:
        return self._registry.get(name)


_LAZY_REGISTRY = LazyModuleRegistry()


def resolve_obj_by_qualname(qualname: str) -> Any:
    """Resolve an object given a dotted qualname like 'module:Class' or 'module.Class'."""
    if ":" in qualname:
        module_name, obj_name = qualname.split(":", 1)
    else:
        parts = qualname.rsplit(".", 1)
        if len(parts) == 2:
            module_name, obj_name = parts
        else:
            module_name, obj_name = parts[0], ""
    mod = import_module(module_name)
    return getattr(mod, obj_name) if obj_name else mod


def resolve_obj_by_qualname_parts(parts: list[str]) -> Any:
    """Resolve object by qualname parts list."""
    if not parts:
        raise ValueError("Empty qualname parts")
    mod = import_module(parts[0])
    obj = mod
    for p in parts[1:]:
        obj = getattr(obj, p)
    return obj


def lazy_import(module_name: str) -> Any:
    """Return module object if present, else a placeholder."""
    present, ver = ensure_module(module_name)
    if present:
        return import_module(module_name)
    return PlaceholderModule(name=module_name, __version__=ver)


def safe_import(module_name: str) -> Optional[ModuleType]:
    try:
        return import_module(module_name)
    except Exception:
        return None


def register_lazy_module(name: str, module: Any) -> None:
    _LAZY_REGISTRY.register(name, module)


def get_lazy_module(name: str) -> Any:
    return _LAZY_REGISTRY.get(name)


def is_module_available(module_name: str) -> bool:
    present, _ = ensure_module(module_name)
    return present


def require_module(module_name: str) -> None:
    if not is_module_available(module_name):
        raise ImportError(f"Required module {module_name} not available")


__all__ = [
    "PlaceholderModule",
    "LazyModuleRegistry",
    "LazyAttribute",
    "import_from_path",
    "import_from_module",
    "reload_module",
    "unload_module",
    "get_module_version",
    "compare_versions",
    "ensure_module",
    "resolve_obj_by_qualname",
    "resolve_obj_by_qualname_parts",
    "lazy_import",
    "safe_import",
    "register_lazy_module",
    "get_lazy_module",
    "is_module_available",
    "require_module",
]
