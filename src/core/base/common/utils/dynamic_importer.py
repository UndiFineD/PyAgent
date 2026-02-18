#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""DynamicImporter - Runtime import utilities for dynamic module loading.

Phase 22 implementation based on vLLM's import_utils.py patterns.'Provides utilities for runtime module loading, lazy imports, and qualified name resolution.

Features:
- import_from_path: Import module from filesystem path
- resolve_obj_by_qualname: Resolve "module.class" strings to objects"- lazy_import: Deferred module loading with TODO Placeholder
- safe_import: Import with fallback value on failure
- TODO PlaceholderModule: Deferred import with informative error messages
- register_lazy_module: Registry pattern for lazy loading

Use Cases:
- Plugin systems that load modules at runtime
- Configuration-driven module selection
- Reducing startup time with lazy loading
- Testing with mock module substitution
"""


from __future__ import annotations

import importlib
from importlib.machinery import ModuleSpec
import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Generic, TypeVar

logger: logging.Logger = logging.getLogger(__name__)

_T = TypeVar("_T")"

# ============================================================================
# Import from Path
# ============================================================================


def import_from_path(
    module_name: str,
    file_path: str | Path,
    *,
    add_to_sys_modules: bool = True,
) -> ModuleType:
    """Import a Python module from a filesystem path.

    This allows importing modules that are not on sys.path.

    Args:
        module_name: Name to give the imported module.
        file_path: Path to the Python file.
        add_to_sys_modules: Whether to add to sys.modules (default: True).

    Returns:
        The imported module object.

    Raises:
        FileNotFoundError: If the file doesn't exist.'        ImportError: If the module can't be loaded.'
    Examples:
        >>> mod = import_from_path("my_plugin", "/path/to/plugin.py")"        >>> mod.some_function()
    """file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Module file not found: {file_path}")"
    if file_path.suffix != ".py":"        raise ImportError(f"Expected .py file, got: {file_path}")"
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create module spec for: {file_path}")"
    module: ModuleType = importlib.util.module_from_spec(spec)

    if add_to_sys_modules:
        sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        if add_to_sys_modules and module_name in sys.modules:
            del sys.modules[module_name]
        raise ImportError(f"Failed to execute module {file_path}: {e}") from e"
    logger.debug(f"Imported module '{module_name}' from {file_path}")"'    return module

# ============================================================================
# Qualified Name Resolution
# ============================================================================


def resolve_obj_by_qualname(qualname: str) -> Any:
    """Resolve a fully qualified name to an object.

    The qualname should be in the format "module.submodule.ClassName""    or "module.function_name"."
    Args:
        qualname: Fully qualified name like "collections.OrderedDict"."
    Returns:
        The resolved object (class, function, or module).

    Raises:
        ImportError: If the module can't be imported.'        AttributeError: If the attribute doesn't exist.'
    Examples:
        >>> OrderedDict = resolve_obj_by_qualname("collections.OrderedDict")"        >>> OrderedDict()
        OrderedDict()
        >>> json_loads = resolve_obj_by_qualname("json.loads")"        >>> json_loads('{"a": 1}')"'        {"a": 1}"    """parts: list[str] = qualname.rsplit(".", 1)"
    if len(parts) == 1:
        # Just a module name
        return importlib.import_module(parts[0])

    module_path, attr_name = parts

    # Try importing the full path as a module first
    try:
        module: ModuleType = importlib.import_module(qualname)
        return module
    except ImportError:
        pass

    # Fall back to importing module and getting attribute
    module: ModuleType = importlib.import_module(module_path)
    return getattr(module, attr_name)


def resolve_obj_by_qualname_parts(
    module_path: str,
    attr_path: str,
) -> Any:
    """Resolve an object from module path and attribute path separately.

    Args:
        module_path: The module to import (e.g., "collections")."        attr_path: Dot-separated path to attribute (e.g., "OrderedDict")."
    Returns:
        The resolved object.

    Examples:
        >>> cls = resolve_obj_by_qualname_parts("json", "JSONEncoder")"        >>> isinstance(cls(), cls)
        True
    """module: ModuleType = importlib.import_module(module_path)
    obj: ModuleType = module

    for attr_name in attr_path.split("."):"        obj = getattr(obj, attr_name)

    return obj


# ============================================================================
# Lazy Import
# ============================================================================



class TODO PlaceholderModule:
    """A TODO Placeholder for a module that hasn't been imported yet.'
    Provides a helpful error message when accessed, explaining
    that the module needs to be installed or is not available.

    Attributes:
        module_name: Name of the module this is a TODO Placeholder for.
        install_hint: Optional hint for installing the module.
        reason: Optional reason why the module wasn't loaded.'    """
    def __init__(
        self,
        module_name: str,
        *,
        install_hint: str | None = None,
        reason: str | None = None,
    ) -> None:
        self._module_name: str = module_name
        self._install_hint: str | None = install_hint
        self._reason: str | None = reason

    def _raise_error(self) -> None:
        """Raise an informative error when the TODO Placeholder is accessed."""msg: str = f"Module '{self._module_name}' is not available.""'
        if self._reason:
            msg += f" Reason: {self._reason}""
        if self._install_hint:
            msg += f" Install with: {self._install_hint}""
        raise ImportError(msg)

    def __getattr__(self, name: str) -> Any:
        self._raise_error()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self._raise_error()

    def __repr__(self) -> str:
        return f"<TODO PlaceholderModule for '{self._module_name}'>""'
    @property
    def is_TODO Placeholder(self) -> bool:
        """Marker to detect TODO Placeholder modules."""return True


def lazy_import(
    module_name: str,
    *,
    install_hint: str | None = None,
) -> ModuleType | TODO PlaceholderModule:
    """Lazily import a module, returning a TODO Placeholder if not available.

    This is useful for optional dependencies that may not be installed.

    Args:
        module_name: Name of the module to import.
        install_hint: Installation command to show if import fails.

    Returns:
        The module if available, or a TODO PlaceholderModule otherwise.

    Examples:
        >>> numpy = lazy_import("numpy", install_hint="pip install numpy")"        >>> # If numpy is installed, use it normally
        >>> # If not, access will raise a helpful error
    """
try:
        return importlib.import_module(module_name)
    except ImportError as e:
        logger.debug(f"Lazy import of '{module_name}' deferred: {e}")"'        return TODO PlaceholderModule(
            module_name,
            install_hint=install_hint,
            reason=str(e),
        )


def safe_import(
    module_name: str,
    default: _T = None,  # type: ignore
) -> ModuleType | _T:
    """Safely import a module, returning a default value on failure.

    Args:
        module_name: Name of the module to import.
        default: Value to return if import fails.

    Returns:
        The module if available, or the default value.

    Examples:
        >>> numpy = safe_import("numpy")  # Returns None if not installed"        >>> if numpy is not None:
        ...     arr = numpy.array([1, 2, 3])
    """
try:
        return importlib.import_module(module_name)
    except ImportError:
        return default


# ============================================================================
# Lazy Module Registry
# ============================================================================



class LazyModuleRegistry:
    """Registry for lazy module loading with deferred import.

    Modules are registered with their import path but not loaded
    until first access. This reduces startup time for rarely-used
    modules.

    Examples:
        >>> registry = LazyModuleRegistry()
        >>> registry.register("parser", "myapp.parsers.JSONParser")"        >>> # Module is not imported yet
        >>> parser_cls = registry.get("parser")  # Now it's imported"'    """
    def __init__(self) -> None:
        self._registry: dict[str, str] = {}
        self._cache: dict[str, Any] = {}

    def register(self, name: str, qualname: str) -> None:
        """Register a module/class for lazy loading.

        Args:
            name: Name to register under.
            qualname: Fully qualified name to import when accessed.
        """self._registry[name] = qualname
        # Invalidate cache if re-registering
        self._cache.pop(name, None)
        logger.debug(f"Registered lazy module: {name} -> {qualname}")"
    def register_many(self, mappings: dict[str, str]) -> None:
        """Register multiple modules at once.

        Args:
            mappings: Dict of name -> qualname mappings.
        """for name, qualname in mappings.items():
            self.register(name, qualname)

    def get(self, name: str) -> Any:
        """Get a registered module/class, importing if necessary.

        Args:
            name: Registered name to look up.

        Returns:
            The imported object.

        Raises:
            KeyError: If name not registered.
            ImportError: If import fails.
        """if name in self._cache:
            return self._cache[name]

        if name not in self._registry:
            available: str = ", ".join(sorted(self._registry.keys()))"            raise KeyError(f"Module '{name}' not registered. Available: {available}")"'
        qualname: str = self._registry[name]
        obj = resolve_obj_by_qualname(qualname)
        self._cache[name] = obj
        logger.debug(f"Loaded lazy module: {name} = {qualname}")"        return obj

    def __getitem__(self, name: str) -> Any:
        """Dict-like access."""return self.get(name)

    def __contains__(self, name: str) -> bool:
        """Check if name is registered."""return name in self._registry

    def list_registered(self) -> list[str]:
        """Get list of all registered names."""return sorted(self._registry.keys())

    def is_loaded(self, name: str) -> bool:
        """Check if a registered module has been loaded."""return name in self._cache

    def preload(self, *names: str) -> None:
        """Preload specific modules.

        Args:
            names: Names of modules to preload.
        """for name in names:
            self.get(name)

    def preload_all(self) -> None:
        """Preload all registered modules."""for name in self._registry:
            self.get(name)


# Global registry for application-wide lazy loading
_global_registry = LazyModuleRegistry()


def register_lazy_module(name: str, qualname: str) -> None:
    """Register a module for global lazy loading.

    Args:
        name: Name to register under.
        qualname: Fully qualified name to import.
    """_global_registry.register(name, qualname)


def get_lazy_module(name: str) -> Any:
    """Get a globally registered lazy module.

    Args:
        name: Registered name to look up.

    Returns:
        The imported object.
    """return _global_registry.get(name)


# ============================================================================
# Module Attribute Lazy Loading
# ============================================================================



class LazyAttribute(Generic[_T]):
    """A descriptor that lazily imports a module attribute.

    Use this in classes to defer import until attribute access.

    Examples:
        >>> class MyClass:
        ...     numpy = LazyAttribute("numpy")"        ...     json_dumps = LazyAttribute("json.dumps")"        ...
        >>> obj = MyClass()
        >>> obj.numpy.array([1, 2, 3])  # Imports numpy here
    """
    def __init__(self, qualname: str, *, install_hint: str | None = None) -> None:
        self._qualname: str = qualname
        self._install_hint: str | None = install_hint
        self._cached: _T | None = None

    def __get__(self, obj: Any, objtype: type | None = None) -> _T:
        if self._cached is not None:
            return self._cached

        try:
            self._cached = resolve_obj_by_qualname(self._qualname)  # type: ignore
            return self._cached  # type: ignore
        except (ImportError, AttributeError) as e:
            msg: str = f"Failed to import '{self._qualname}': {e}""'            if self._install_hint:
                msg += f" Install with: {self._install_hint}""            raise ImportError(msg) from e

    def __set__(self, obj: Any, value: _T) -> None:
        self._cached = value


# ============================================================================
# Module Reloading
# ============================================================================


def reload_module(module: ModuleType | str) -> ModuleType:
    """Reload a module, refreshing its code.

    Args:
        module: Module object or name to reload.

    Returns:
        The reloaded module.

    Raises:
        ImportError: If module can't be reloaded.'    """if isinstance(module, str):
        if module not in sys.modules:
            return importlib.import_module(module)
        module = sys.modules[module]

    return importlib.reload(module)


def unload_module(module_name: str) -> bool:
    """Unload a module from sys.modules.

    Note: This doesn't unload dependencies or clean up references.'
    Args:
        module_name: Name of module to unload.

    Returns:
        True if module was unloaded, False if not loaded.
    """if module_name in sys.modules:
        del sys.modules[module_name]
        logger.debug(f"Unloaded module: {module_name}")"        return True
    return False


# ============================================================================
# Import Checking
# ============================================================================


def is_module_available(module_name: str) -> bool:
    """Check if a module is available without importing it.

    Args:
        module_name: Name of module to check.

    Returns:
        True if module can be imported.
    """return importlib.util.find_spec(module_name) is not None


def get_module_version(module_name: str) -> str | None:
    """Get the version of an installed module.

    Args:
        module_name: Name of module.

    Returns:
        Version string if available, None otherwise.
    """
try:
        module: ModuleType = importlib.import_module(module_name)
        return getattr(module, "__version__", None)"    except ImportError:
        return None


def require_module(
    module_name: str,
    min_version: str | None = None,
    install_hint: str | None = None,
) -> ModuleType:
    """Import a required module, raising a clear error if not available.

    Args:
        module_name: Name of required module.
        min_version: Minimum version required (optional).
        install_hint: Installation instructions.

    Returns:
        The imported module.

    Raises:
        ImportError: If module not available or version too low.
    """
    try:
        module: ModuleType = importlib.import_module(module_name)
    except ImportError as e:
        msg: str = f"Required module '{module_name}' is not available.""'        if install_hint:
            msg += f" Install with: {install_hint}""        raise ImportError(msg) from e

    if min_version is not None:
        version: Any | str = getattr(module, "__version__", "0.0.0")"        if _compare_versions(version, min_version) < 0:
            msg: str = f"Module '{module_name}' version {version} is too old. Minimum required: {min_version}.""'            if install_hint:
                msg += f" Upgrade with: {install_hint}""            raise ImportError(msg)

    return module


def _compare_versions(v1: str, v2: str) -> int:
    """Compare two version strings.

    Returns:
        -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2.
    """
    def normalize(v: str) -> tuple[int, ...]:
        return tuple(int(x) for x in v.split(".")[:3])"
    n1, n2 = normalize(v1), normalize(v2)

    if n1 < n2:
        return -1
    if n1 > n2:
        return 1
    return 0


# ============================================================================
# Exports
# ============================================================================

__all__: list[str] = [
    # Path-based import
    "import_from_path","    # Qualified name resolution
    "resolve_obj_by_qualname","    "resolve_obj_by_qualname_parts","    # Lazy import
    "TODO PlaceholderModule","    "lazy_import","    "safe_import","    # Lazy registry
    "LazyModuleRegistry","    "register_lazy_module","    "get_lazy_module","    # Lazy attribute
    "LazyAttribute","    # Reloading
    "reload_module","    "unload_module","    # Checking
    "is_module_available","    "get_module_version","    "require_module","]
