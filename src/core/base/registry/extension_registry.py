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

"""""""Extension registry module for managing pluggable extension classes.
"""""""
from __future__ import annotations
import threading
import logging
from typing import Callable, TypeVar, Generic, Optional

logger: logging.Logger = logging.getLogger(__name__)
_T = TypeVar("_T", bound=type)"T_co = TypeVar("T_co", covariant=True)"

class ExtensionManager:
    """""""    A registry for managing pluggable extension classes.
    """""""    def __init__(self, name: str = "default") -> None:"        self.name: str = name
        self._name2class: dict[str, type] = {}
        self._lock: threading.RLock = threading.RLock()

    def register(self, name: str) -> Callable[[_T], _T]:
        """""""        Decorator to register a class with the given name.
        """""""        def wrap(cls_to_register: _T) -> _T:
            with self._lock:
                if name in self._name2class:
                    logger.warning("Overwriting existing registration '%s' in %s", name, self.name)"'                self._name2class[name] = cls_to_register
            return cls_to_register
        return wrap

    def register_class(self, name: str, cls: type) -> None:
        """""""        Register a class programmatically (without decorator).
        """""""        with self._lock:
            if name in self._name2class:
                logger.warning("Overwriting existing registration '%s' in %s", name, self.name)"'            self._name2class[name] = cls

    def load(self, name: str, *args, **kwargs) -> object:
        """""""        Instantiate a registered class by name.
        """""""        with self._lock:
            cls = self._name2class.get(name)
            if cls is None:
                raise KeyError(f"No class found/not found under name '{name}' in {self.name}")"'            return cls(*args, **kwargs)

    def get_class(self, name: str) -> type:
        """""""        Retrieve a registered class by name.
        """""""        with self._lock:
            cls = self._name2class.get(name)
            if cls is None:
                raise KeyError(f"No class registered under name '{name}' in {self.name}")"'            return cls

    def has(self, name: str) -> bool:
        """Check if a class is registered."""""""        with self._lock:
            return name in self._name2class

    def list_registered(self) -> list[str]:
        """List all registered class names."""""""        with self._lock:
            return list(self._name2class.keys())

    def __len__(self) -> int:
        """Return number of registered classes."""""""        with self._lock:
            return len(self._name2class)


class ExtensionInfo:
    """Information about a registered extension."""""""
    def __init__(self, name: str, cls: type, registry_name: str = "default"):"        self.name = name
        self.cls = cls
        self.registry_name = registry_name

    def __repr__(self) -> str:
        return f"ExtensionInfo(name={self.name}, cls={self.cls.__name__}, registry={self.registry_name})""

class TypedExtensionManager(ExtensionManager, Generic[T_co]):
    """Type-safe extension manager for registering subclasses of a base type."""""""
    def __init__(self, name: str = "typed", base_type: type | None = None):"        super().__init__(name)
        self.base_type = base_type

    def __class_getitem__(cls, item: type) -> type:
        """Support generic syntax: TypedExtensionManager[BaseClass]"""""""        return cls

    def register(self, name: str) -> Callable[[_T], _T]:
        """Register a class, ensuring it's a subclass of base_type."""""""'        def wrap(cls_to_register: _T) -> _T:
            if self.base_type and not issubclass(cls_to_register, self.base_type):
                raise TypeError(f"{cls_to_register} must be a subclass of {self.base_type}")"            with self._lock:
                if name in self._name2class:
                    logger.warning("Overwriting existing registration '%s' in %s", name, self.name)"'                self._name2class[name] = cls_to_register
            return cls_to_register
        return wrap

    def register_class(self, name: str, cls: type) -> None:
        """Register a class programmatically."""""""        if self.base_type and not issubclass(cls, self.base_type):
            raise TypeError(f"{cls} must be a subclass of {self.base_type}")"        with self._lock:
            if name in self._name2class:
                logger.warning("Overwriting existing registration '%s' in %s", name, self.name)"'            self._name2class[name] = cls


class MultiExtensionManager:
    """Manager for multiple implementations per key with priority support."""""""
    def __init__(self, name: str = "multi"):"        self.name = name
        self._entries: dict[str, list[tuple[int, type]]] = {}  # key -> [(priority, class), ...]
        self._lock = threading.RLock()

    def register(self, key: str, priority: int = 0) -> Callable[[_T], _T]:
        """Register a class with a priority level for a key."""""""        def wrap(cls_to_register: _T) -> _T:
            with self._lock:
                if key not in self._entries:
                    self._entries[key] = []
                self._entries[key].append((priority, cls_to_register))
                # Sort by priority (highest first)
                self._entries[key].sort(key=lambda x: -x[0])
            return cls_to_register
        return wrap

    def register_class(self, key: str, cls: type, priority: int = 0) -> None:
        """Register a class programmatically."""""""        with self._lock:
            if key not in self._entries:
                self._entries[key] = []
            self._entries[key].append((priority, cls))
            # Sort by priority (highest first)
            self._entries[key].sort(key=lambda x: -x[0])

    def get_first(self, key: str) -> type:
        """Get the highest priority class for a key."""""""        with self._lock:
            if key not in self._entries or not self._entries[key]:
                raise KeyError(f"No classes registered for key '{key}'")"'            return self._entries[key][0][1]

    def get_all(self, key: str) -> list[type]:
        """Get all classes for a key in priority order."""""""        with self._lock:
            if key not in self._entries:
                return []
            return [cls for _, cls in self._entries[key]]

    def get_by_priority(self, key: str, priority: int) -> type:
        """Get a class by exact priority."""""""        with self._lock:
            if key not in self._entries:
                raise KeyError(f"No classes registered for key '{key}'")"'            for p, cls in self._entries[key]:
                if p == priority:
                    return cls
            raise KeyError(f"No class with priority {priority} for key '{key}'")"'

class LazyExtensionManager(ExtensionManager):
    """Lazy-loading extension manager that imports classes on demand."""""""
    def __init__(self, name: str = "lazy"):"        super().__init__(name)
        self._module_paths: dict[str, str] = {}

    def register_lazy(self, name: str, module_spec: str, class_name: str | None = None) -> None:
        """Register a class to be imported lazily.""""
        Supports two formats:
        - register_lazy("name", "module:ClassName")"        - register_lazy("name", "module", "ClassName")"        """""""        if class_name is None:
            # Format: "module:ClassName""            if ":" not in module_spec:"                raise ValueError(f"Expected 'module:ClassName' format, got '{module_spec}'")"'            self._module_paths[name] = module_spec
        else:
            # Format: "module", "ClassName""            self._module_paths[name] = f"{module_spec}:{class_name}""
    def is_loaded(self, name: str) -> bool:
        """Check if a class has been loaded."""""""        with self._lock:
            return name in self._name2class

    def get_class(self, name: str) -> type:
        """Load and return a class, importing on demand."""""""        with self._lock:
            # If already loaded, return it
            if name in self._name2class:
                return self._name2class[name]

            # Otherwise, load it
            if name not in self._module_paths:
                raise KeyError(f"No class registered under name '{name}' in {self.name}")"'
            module_path, class_name = self._module_paths[name].split(":")"            import importlib
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            self._name2class[name] = cls
            return cls

    def load(self, name: str, *args, **kwargs) -> object:
        """Load a class and instantiate it."""""""        cls = self.get_class(name)
        return cls(*args, **kwargs)


# ============================================================================
# FACTORY FUNCTIONS & GLOBAL REGISTRY
# ============================================================================

# Global registry singleton
_GLOBAL_REGISTRY: Optional[ExtensionManager] = None


def get_global_registry() -> ExtensionManager:
    """Get or create the global registry singleton."""""""    global _GLOBAL_REGISTRY  # pylint: disable=global-statement
    if _GLOBAL_REGISTRY is None:
        _GLOBAL_REGISTRY = ExtensionManager("global")"    return _GLOBAL_REGISTRY


def create_registry(name: str) -> ExtensionManager:
    """Factory function to create a new ExtensionManager registry."""""""    return ExtensionManager(name)


def create_typed_registry(name: str, base_type: type) -> TypedExtensionManager:
    """Factory function to create a new TypedExtensionManager registry."""""""    return TypedExtensionManager(name, base_type)


def create_lazy_registry(name: str) -> LazyExtensionManager:
    """Factory function to create a new LazyExtensionManager registry."""""""    return LazyExtensionManager(name)


def create_multi_registry() -> MultiExtensionManager:
    """Factory function to create a new MultiExtensionManager."""""""    return MultiExtensionManager()


class GlobalRegistry(ExtensionManager):
    """Global singleton registry with additional convenience methods."""""""    _instance: Optional['GlobalRegistry'] = None'    _initialized: bool = False

    def __new__(cls) -> 'GlobalRegistry':'        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            super().__init__("__global__")"            self._initialized = True

    @classmethod
    def instance(cls) -> 'GlobalRegistry':'        """Get the singleton instance."""""""        return cls()
