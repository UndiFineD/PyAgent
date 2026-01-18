# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Lazy loading utilities for PyAgent.

This module provides utilities for deferred imports to improve startup time
and reduce memory usage by only loading modules when they are first accessed.

Example usage:

    # Using LazyLoader descriptor
    class MyModule:
        heavy_module = LazyLoader("some.heavy.module", "HeavyClass")

    # Using lazy_import decorator
    @lazy_import
    def get_heavy_class():
        from some.heavy.module import HeavyClass
        return HeavyClass

    # Using ModuleLazyLoader for __getattr__ pattern
    _lazy_modules = ModuleLazyLoader({
        "HeavyClass": ("some.heavy.module", "HeavyClass"),
        "AnotherClass": ("another.module", "AnotherClass"),
    })

    def __getattr__(name: str):
        return _lazy_modules.load(name)
"""

from __future__ import annotations

import importlib
import sys
from functools import lru_cache
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

__all__ = [
    "LazyLoader",
    "lazy_import",
    "ModuleLazyLoader",
]

T = TypeVar("T")


class LazyLoader:
    """
    A descriptor class for deferred imports.

    LazyLoader delays the import of a module/attribute until first access,
    reducing startup time for modules with expensive imports.

    Attributes:
        module_path: The full dotted path to the module containing the target.
        attr_name: The name of the attribute to import from the module.
                   If None, imports the module itself.

    Example:
        class MyClass:
            # Lazy load pandas DataFrame
            DataFrame = LazyLoader("pandas", "DataFrame")

            # Lazy load entire module
            numpy = LazyLoader("numpy")

        # DataFrame is only imported when first accessed
        df = MyClass.DataFrame()
    """

    def __init__(
        self,
        module_path: str,
        attr_name: Optional[str] = None,
        *,
        doc: Optional[str] = None,
    ) -> None:
        """
        Initialize the LazyLoader.

        Args:
            module_path: The dotted path to the module (e.g., "pandas.core").
            attr_name: The name of the attribute to import from the module.
                       If None, the entire module is returned.
            doc: Optional docstring for the descriptor.
        """
        self.module_path = module_path
        self.attr_name = attr_name
        self._cached: Optional[Any] = None
        self._loaded = False
        self.__doc__ = doc or f"Lazy loader for {module_path}.{attr_name or ''}"

    def _load(self) -> Any:
        """Load and cache the module/attribute."""
        if not self._loaded:
            module = importlib.import_module(self.module_path)
            if self.attr_name:
                self._cached = getattr(module, self.attr_name)
            else:
                self._cached = module
            self._loaded = True
        return self._cached

    def __get__(self, obj: Optional[object], objtype: Optional[type] = None) -> Any:
        """
        Descriptor protocol implementation for attribute access.

        Args:
            obj: The instance accessing the descriptor, or None for class access.
            objtype: The type of the instance.

        Returns:
            The loaded module or attribute.
        """
        return self._load()

    def __repr__(self) -> str:
        status = "loaded" if self._loaded else "not loaded"
        target = f"{self.module_path}.{self.attr_name}" if self.attr_name else self.module_path
        return f"<LazyLoader({target!r}) [{status}]>"


def lazy_import(func: Callable[[], T]) -> Callable[[], T]:
    """
    Decorator that wraps a function with lru_cache for lazy, cached imports.

    This decorator is useful for creating factory functions that lazily
    import and return expensive modules or classes. The result is cached
    after the first call.

    Args:
        func: A callable that performs the import and returns the result.

    Returns:
        A wrapped function that caches the import result.

    Example:
        @lazy_import
        def get_numpy():
            '''Lazily import numpy.'''
            import numpy as np
            return np

        # First call imports numpy
        np = get_numpy()

        # Subsequent calls return cached module
        np2 = get_numpy()  # Same object, no re-import
    """
    cached_func = lru_cache(maxsize=1)(func)

    def wrapper() -> T:
        return cached_func()

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    wrapper.__wrapped__ = func  # type: ignore[attr-defined]
    return wrapper


class ModuleLazyLoader:
    """
    A utility class for implementing module-level __getattr__ lazy loading.

    This class provides a clean way to implement the PEP 562 __getattr__ pattern
    for lazy loading of module-level attributes. It maintains a registry of
    lazy imports and handles loading on first access.

    Attributes:
        _registry: A dictionary mapping attribute names to (module_path, attr_name) tuples.
        _cache: A dictionary caching loaded attributes.

    Example:
        # In your module's __init__.py:
        from src.core.lazy_loader import ModuleLazyLoader

        _lazy = ModuleLazyLoader({
            "EagleProposer": ("src.infrastructure.speculative_v2.EagleProposer", "EagleProposer"),
            "ARCOffloadManager": ("src.infrastructure.kv_transfer.ARCOffloadManager", "ARCOffloadManager"),
        })

        def __getattr__(name: str):
            return _lazy.load(name)

        def __dir__():
            return list(globals().keys()) + _lazy.available_names()
    """

    def __init__(
        self,
        registry: Dict[str, Tuple[str, str]],
        *,
        parent_module: Optional[str] = None,
    ) -> None:
        """
        Initialize the ModuleLazyLoader.

        Args:
            registry: A dictionary mapping attribute names to tuples of
                      (module_path, attribute_name) for lazy loading.
            parent_module: Optional parent module name for relative imports.
        """
        self._registry = registry
        self._cache: Dict[str, Any] = {}
        self._parent_module = parent_module

    def load(self, name: str) -> Any:
        """
        Load and return the requested attribute.

        Args:
            name: The name of the attribute to load.

        Returns:
            The loaded attribute.

        Raises:
            AttributeError: If the name is not in the registry.
        """
        if name in self._cache:
            return self._cache[name]

        if name not in self._registry:
            raise AttributeError(f"module has no attribute {name!r}")

        module_path, attr_name = self._registry[name]

        # Handle relative imports if parent_module is set
        if self._parent_module and module_path.startswith("."):
            module_path = self._parent_module + module_path

        try:
            module = importlib.import_module(module_path)
            attr = getattr(module, attr_name)
            self._cache[name] = attr
            return attr
        except ImportError as e:
            raise ImportError(
                f"Failed to lazy import {name!r} from {module_path}: {e}"
            ) from e
        except AttributeError as e:
            raise AttributeError(
                f"Module {module_path!r} has no attribute {attr_name!r}: {e}"
            ) from e

    def available_names(self) -> list[str]:
        """
        Return a list of all attribute names available for lazy loading.

        Returns:
            List of attribute names in the registry.
        """
        return list(self._registry.keys())

    def is_loaded(self, name: str) -> bool:
        """
        Check if an attribute has been loaded.

        Args:
            name: The name of the attribute to check.

        Returns:
            True if the attribute is in the cache, False otherwise.
        """
        return name in self._cache

    def preload(self, *names: str) -> None:
        """
        Preload specified attributes into the cache.

        Args:
            *names: The names of attributes to preload.
                    If no names are provided, all attributes are preloaded.
        """
        target_names = names if names else self._registry.keys()
        for name in target_names:
            if name in self._registry:
                self.load(name)

    def clear_cache(self) -> None:
        """Clear the cache of loaded attributes."""
        self._cache.clear()

    def __contains__(self, name: str) -> bool:
        """Check if a name is in the registry."""
        return name in self._registry

    def __repr__(self) -> str:
        loaded = len(self._cache)
        total = len(self._registry)
        return f"<ModuleLazyLoader({loaded}/{total} loaded)>"
