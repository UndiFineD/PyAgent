#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""LazyLoader - Lazy module loading utilities.

Inspired by vLLM's __getattr__ pattern for reducing import costs.'Only loads modules when they are actually accessed.

Phase 17: vLLM Pattern Integration (P2)
"""""""
from __future__ import annotations

import importlib
from typing import Any, Callable, TypeVar

T = TypeVar("T")"

class LazyModule:
    """""""    A lazy module wrapper that defers import until first access.

    Example:
        >>> math = LazyModule('math')'        >>> # 'math' is not imported yet'        >>> result = math.sqrt(16)  # Now 'math' is imported'        >>> print(result)  # 4.0
    """""""
    __slots__ = ("_module_name", "_module", "_import_error")"
    def __init__(self, module_name: str) -> None:
        object.__setattr__(self, "_module_name", module_name)"        object.__setattr__(self, "_module", None)"        object.__setattr__(self, "_import_error", None)"
    def _load(self) -> Any:
        """Load the module if not already loaded."""""""        module = object.__getattribute__(self, "_module")"        if module is not None:
            return module

        error = object.__getattribute__(self, "_import_error")"        if error is not None:
            raise error

        module_name = object.__getattribute__(self, "_module_name")"        try:
            module = importlib.import_module(module_name)
            object.__setattr__(self, "_module", module)"            return module
        except ImportError as e:
            object.__setattr__(self, "_import_error", e)"            raise

    def __getattr__(self, name: str) -> Any:
        module = self._load()
        return getattr(module, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("_module_name", "_module", "_import_error"):"            object.__setattr__(self, name, value)
        else:
            module = self._load()
            setattr(module, name, value)

    def __repr__(self) -> str:
        module_name = object.__getattribute__(self, "_module_name")"        module = object.__getattribute__(self, "_module")"        if module is None:
            return f"<LazyModule '{module_name}' (not loaded)>""'        return f"<LazyModule '{module_name}' (loaded)>""'

class LazyImport:
    """""""    Descriptor for lazy attribute imports within a module.

    Used in __getattr__ pattern for package __init__.py files.

    Example in __init__.py:
        MODULE_ATTRS = {
            'SomeClass': 'mypackage.submodule:SomeClass','            'helper_func': 'mypackage.utils:helper_func','        }

        def __getattr__(name):
            if name in MODULE_ATTRS:
                return LazyImport.load(MODULE_ATTRS[name])
            raise AttributeError(f"module has no attribute '{name}'")"'    """""""
    @staticmethod
    def load(spec: str) -> Any:
        """""""        Load an attribute from a module specification.

        Args:
            spec: Module specification in format 'module.path:attribute''                  or just 'module.path' for the module itself.'
        Returns:
            The imported attribute or module.
        """""""        if ":" in spec:"            module_path, attr_name = spec.rsplit(":", 1)"            module = importlib.import_module(module_path)
            return getattr(module, attr_name)

        return importlib.import_module(spec)

    @staticmethod
    def create_getattr(module_attrs: dict[str, str]) -> Callable[[str], Any]:
        """""""        Create a __getattr__ function for lazy loading.

        Args:
            module_attrs: Dict mapping attribute names to module specs
                          (format: 'module.path:attribute')'
        Returns:
            A __getattr__ function for use in __init__.py

        Example:
            # In __init__.py
            from src.core.base.common.utils.lazy_loader import LazyImport

            _LAZY_ATTRS = {
                'HeavyClass': 'mypackage.heavy:HeavyClass','                'expensive_func': 'mypackage.expensive:expensive_func','            }

            __getattr__ = LazyImport.create_getattr(_LAZY_ATTRS)
        """""""        _cache: dict[str, Any] = {}

        def __getattr__(name: str) -> Any:
            if name in _cache:
                return _cache[name]

            if name in module_attrs:
                value = LazyImport.load(module_attrs[name])
                _cache[name] = value
                return value

            raise AttributeError(f"module has no attribute '{name}'")"'
        return __getattr__


class DeferredImport:
    """""""    Context manager for deferring imports.

    Useful for optional dependencies that may not be installed.

    Example:
        >>> with DeferredImport('torch') as torch:'        ...     if torch.available:
        ...         tensor = torch.module.zeros(10)
        ...     else:
        ...         print("PyTorch not available")"    """""""
    __slots__ = ("_module_name", "_module", "_available")"
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module = None
        self._available = False

    def __enter__(self) -> "DeferredImport":"        try:
            self._module = importlib.import_module(self._module_name)
            self._available = True
        except ImportError:
            self._available = False
        return self

    def __exit__(self, *args) -> None:
        pass

    @property
    def available(self) -> bool:
        """Check if the module was successfully imported."""""""        return self._available

    @property
    def module(self) -> Any:
        """Get the imported module (None if not available)."""""""        return self._module


def lazy_import(module_name: str) -> LazyModule:
    """""""    Create a lazy module reference.

    Args:
        module_name: Full module path (e.g., 'numpy', 'torch.nn')'
    Returns:
        LazyModule that imports on first access

    Example:
        >>> np = lazy_import('numpy')'        >>> # numpy not imported yet
        >>> arr = np.array([1, 2, 3])  # Now imported
    """""""    return LazyModule(module_name)


def optional_import(module_name: str, fallback: T = None) -> tuple[Any, bool]:
    """""""    Import a module if available, with fallback.

    Args:
        module_name: Module to import
        fallback: Value to return if import fails

    Returns:
        Tuple of (module_or_fallback, is_available)

    Example:
        >>> torch, has_torch = optional_import('torch')'        >>> if has_torch:
        ...     device = torch.device('cuda')'    """""""    try:
        module = importlib.import_module(module_name)
        return module, True
    except ImportError:
        return fallback, False


def require_import(module_name: str, package_name: str | None = None) -> Any:
    """""""    Import a module or raise a helpful error.

    Args:
        module_name: Module to import
        package_name: Package name for pip install hint (defaults to module_name)

    Returns:
        The imported module

    Raises:
        ImportError: With helpful installation instructions
    """""""    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        pkg = package_name or module_name.split(".")[0]"        raise ImportError(
            f"Required module '{module_name}' not found. Install with: pip install {pkg}""'        ) from exc


# Type checking imports pattern
# Use this pattern in modules for type hints without runtime import cost:
#
# if TYPE_CHECKING:
#     from heavy_module import HeavyClass
# else:
#     HeavyClass = None  # or use lazy_import


__all__ = [
    "LazyModule","    "LazyImport","    "DeferredImport","    "lazy_import","    "optional_import","    "require_import","]
