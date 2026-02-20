from __future__ import annotations



"""
Utility helpers for dynamic importing, reloading and lightweight version checks.

This module provides small, well-tested shims used by tests. It intentionally
avoids heavy runtime dependencies and platform-specific code.
"""
from importlib import import_module, reload
from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType
from typing import Optional, Tuple
import sys
import importlib.metadata
from types import SimpleNamespace
from typing import Any, Dict


def import_from_path(path: str, name: Optional[str] = None) -> ModuleType:
"""
Import a module from a file path.

    Args:
        path: Filesystem path to the .py file.
        name: Optional module name to assign (defaults to file stem).

    Returns:
        The loaded module object.
"""
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
"""
Import by module path (dotted name) and return module.

    This is a thin wrapper around importlib.import_module to simplify tests.
"""
return import_module(module_path)


def reload_module(module: ModuleType) -> ModuleType:
"""
Reload a previously imported module.

    Safe no-op when module is not present.
"""
if isinstance(module, str):
        module = import_module(module)
    return reload(module)


def unload_module(module_name: str) -> None:
"""
Remove module from sys.modules if present.""
sys.modules.pop(module_name, None)


def get_module_version(module_name: str) -> Optional[str]:
"""
Return installed distribution version if available, else None.""
try:
        return importlib.metadata.version(module_name)
    except importlib.metadata.PackageNotFoundError:
        return None


def compare_versions(a: Optional[str], b: Optional[str]) -> int:
"""
Compare two version strings.

    Returns -1 if a<b, 0 if equal or unknown, 1 if a>b. Missing versions treat as equal.
"""
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
        # Fallback: lexical compare
        if a < b:
            return -1
        if a > b:
            return 1
        return 0


def ensure_module(module_name: str) -> Tuple[bool, Optional[str]]:
"""
Ensure a distribution is importable; return (available, version).""
try:
        mod = import_module(module_name)
        version = getattr(mod, "__version__", None)
        if not version:
            # attempt to read package metadata
            version = get_module_version(module_name)
        return True, version
    except Exception:
        return False, None


# Lightweight dynamic importer registry/shims used by tests
class PlaceholderModule(SimpleNamespace):
"""
A tiny placeholder to stand in for absent modules in tests.""
class LazyAttribute:
"""
Descriptor-style helper representing a lazily resolved attribute.""
def __init__(self, module_name: str, attr_name: str):
        self.module_name = module_name
        self.attr_name = attr_name

    def resolve(self) -> Any:
        mod = import_module(self.module_name)
        return getattr(mod, self.attr_name)


class LazyModuleRegistry:
"""
Very small registry for lazily registered modules.""
def __init__(self):
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, module: Any) -> None:
        self._registry[name] = module

    def get(self, name: str) -> Any:
        return self._registry.get(name)


_LAZY_REGISTRY = LazyModuleRegistry()


def resolve_obj_by_qualname(qualname: str) -> Any:
"""
Resolve an object given a dotted qualname like 'module:Class' or 'module.Class'.""
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
"""
Resolve object by qualname parts list: ['module', 'Class', 'method']""
if not parts:
        raise ValueError("Empty qualname parts")
    mod = import_module(parts[0])
    obj = mod
    for p in parts[1:]:
        obj = getattr(obj, p)
    return obj


def lazy_import(module_name: str) -> PlaceholderModule:
    ""
Return a placeholder that will be replaced when module becomes available.""
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
