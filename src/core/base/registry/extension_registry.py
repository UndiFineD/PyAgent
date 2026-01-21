"""
Extension Registry Module - Phase 20: Production Infrastructure
================================================================

Plugin system for managing extensible component registries.
Inspired by vLLM's registry.py pattern.

Features:
- ExtensionManager: Register and instantiate extension classes by name
- TypedExtensionManager: Generic typed extension registry
- MultiExtensionManager: Registry supporting multiple implementations
- @register decorator: Easy class registration
- Lazy instantiation: Classes loaded only when accessed
- Priority ordering: Extensions can define priority

Author: PyAgent Phase 20
"""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    TypeVar,
    Protocol,
    runtime_checkable,
    overload,
)
from functools import wraps

if TYPE_CHECKING:
    from typing import ClassVar

logger = logging.getLogger(__name__)

_T = TypeVar("_T", bound=type)
_V = TypeVar("_V")
_Base = TypeVar("_Base")


# ============================================================================
# Extension Manager (Basic)
# ============================================================================


class ExtensionManager:
    """
    A registry for managing pluggable extension classes.
    
    Provides a simple mechanism to register and instantiate extension classes
    by name. Commonly used for plugin systems where different implementations
    can be swapped at runtime.
    
    Example:
        >>> FOO_REGISTRY = ExtensionManager("foo")
        >>> @FOO_REGISTRY.register("my_impl")
        ... class MyFooImpl:
        ...     def __init__(self, value: int):
        ...         self.value = value
        >>> foo = FOO_REGISTRY.load("my_impl", value=123)
        >>> foo.value
        123
    """
    
    def __init__(self, name: str = "default") -> None:
        """Initialize an empty extension registry."""
        self.name = name
        self._name2class: dict[str, type] = {}
        self._lock = threading.RLock()
    
    def register(self, name: str) -> Callable[[_T], _T]:
        """
        Decorator to register a class with the given name.
        
        Args:
            name: The unique name to register the class under.
            
        Returns:
            Decorator function that registers and returns the class.
        """
        def wrap(cls_to_register: _T) -> _T:
            with self._lock:
                if name in self._name2class:
                    logger.warning(
                        f"Overwriting existing registration '{name}' in {self.name}"
                    )
                self._name2class[name] = cls_to_register
            return cls_to_register
        return wrap
    
    def register_class(self, name: str, cls: type) -> None:
        """
        Register a class programmatically (without decorator).
        
        Args:
            name: The unique name to register the class under.
            cls: The class to register.
        """
        with self._lock:
            if name in self._name2class:
                logger.warning(
                    f"Overwriting existing registration '{name}' in {self.name}"
                )
            self._name2class[name] = cls
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a class by name.
        
        Args:
            name: The name to unregister.
            
        Returns:
            True if the class was unregistered, False if not found.
        """
        with self._lock:
            if name in self._name2class:
                del self._name2class[name]
                return True
            return False
    
    def load(self, cls_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Instantiate and return a registered extension class by name.
        
        Args:
            cls_name: The registered name of the class to instantiate.
            *args: Positional arguments to pass to the constructor.
            **kwargs: Keyword arguments to pass to the constructor.
            
        Returns:
            An instance of the registered class.
            
        Raises:
            KeyError: If the class name is not registered.
        """
        with self._lock:
            cls = self._name2class.get(cls_name)
        if cls is None:
            available = list(self._name2class.keys())
            raise KeyError(
                f"Extension class '{cls_name}' not found in {self.name}. "
                f"Available: {available}"
            )
        return cls(*args, **kwargs)
    
    def get_class(self, cls_name: str) -> type | None:
        """
        Get a registered class without instantiation.
        
        Args:
            cls_name: The registered name of the class.
            
        Returns:
            The class if found, None otherwise.
        """
        with self._lock:
            return self._name2class.get(cls_name)
    
    def has(self, name: str) -> bool:
        """Check if a class is registered under the given name."""
        with self._lock:
            return name in self._name2class
    
    def list_registered(self) -> list[str]:
        """Return a list of all registered class names."""
        with self._lock:
            return list(self._name2class.keys())
    
    def __contains__(self, name: str) -> bool:
        return self.has(name)
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._name2class)
    
    def __repr__(self) -> str:
        return f"ExtensionManager({self.name!r}, registered={len(self)})"


# ============================================================================
# Typed Extension Manager
# ============================================================================


class TypedExtensionManager(Generic[_Base]):
    """
    A type-safe registry for managing extension classes of a specific base type.
    
    Example:
        >>> class BasePlugin(ABC):
        ...     @abstractmethod
        ...     def process(self, data: str) -> str: ...
        >>> PLUGINS = TypedExtensionManager[BasePlugin]("plugins", BasePlugin)
        >>> @PLUGINS.register("upper")
        ... class UpperPlugin(BasePlugin):
        ...     def process(self, data: str) -> str:
        ...         return data.upper()
    """
    
    def __init__(self, name: str, base_class: type[_Base]) -> None:
        """
        Initialize a typed extension registry.
        
        Args:
            name: The name of this registry.
            base_class: The base class/interface all extensions must inherit from.
        """
        self.name = name
        self.base_class = base_class
        self._name2class: dict[str, type[_Base]] = {}
        self._lock = threading.RLock()
    
    def register(self, name: str) -> Callable[[type[_Base]], type[_Base]]:
        """
        Decorator to register a class with type checking.
        
        Validates that the class inherits from the base class.
        """
        def wrap(cls_to_register: type[_Base]) -> type[_Base]:
            if not issubclass(cls_to_register, self.base_class):
                raise TypeError(
                    f"Class {cls_to_register.__name__} must inherit from "
                    f"{self.base_class.__name__}"
                )
            with self._lock:
                if name in self._name2class:
                    logger.warning(
                        f"Overwriting existing registration '{name}' in {self.name}"
                    )
                self._name2class[name] = cls_to_register
            return cls_to_register
        return wrap
    
    def load(self, cls_name: str, *args: Any, **kwargs: Any) -> _Base:
        """Instantiate and return a registered extension."""
        with self._lock:
            cls = self._name2class.get(cls_name)
        if cls is None:
            available = list(self._name2class.keys())
            raise KeyError(
                f"Extension class '{cls_name}' not found in {self.name}. "
                f"Available: {available}"
            )
        return cls(*args, **kwargs)
    
    def get_class(self, cls_name: str) -> type[_Base] | None:
        """Get a registered class without instantiation."""
        with self._lock:
            return self._name2class.get(cls_name)
    
    def has(self, name: str) -> bool:
        """Check if a class is registered under the given name."""
        with self._lock:
            return name in self._name2class
    
    def list_registered(self) -> list[str]:
        """Return a list of all registered class names."""
        with self._lock:
            return list(self._name2class.keys())
    
    def __contains__(self, name: str) -> bool:
        return self.has(name)
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._name2class)


# ============================================================================
# Multi Extension Manager (supports multiple implementations per key)
# ============================================================================


@dataclass
class ExtensionInfo:
    """Metadata for a registered extension."""
    name: str
    cls: type
    priority: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other: "ExtensionInfo") -> bool:
        return self.priority > other.priority  # Higher priority first


class MultiExtensionManager:
    """
    Registry supporting multiple implementations per key with priority ordering.
    
    Useful for plugin systems where multiple handlers can be registered
    for the same extension point.
    
    Example:
        >>> HANDLERS = MultiExtensionManager("handlers")
        >>> @HANDLERS.register("format", priority=10)
        ... class JSONFormatter: ...
        >>> @HANDLERS.register("format", priority=5)
        ... class XMLFormatter: ...
        >>> HANDLERS.get_all("format")  # Returns [JSONFormatter, XMLFormatter]
    """
    
    def __init__(self, name: str = "default") -> None:
        self.name = name
        self._extensions: dict[str, list[ExtensionInfo]] = {}
        self._lock = threading.RLock()
    
    def register(
        self,
        name: str,
        priority: int = 0,
        **metadata: Any
    ) -> Callable[[_T], _T]:
        """
        Decorator to register a class with the given name and priority.
        
        Args:
            name: The extension point name.
            priority: Higher priority extensions are loaded first.
            **metadata: Additional metadata to store with the extension.
        """
        def wrap(cls_to_register: _T) -> _T:
            info = ExtensionInfo(
                name=name,
                cls=cls_to_register,
                priority=priority,
                metadata=metadata,
            )
            with self._lock:
                if name not in self._extensions:
                    self._extensions[name] = []
                self._extensions[name].append(info)
                self._extensions[name].sort()  # Sort by priority
            return cls_to_register
        return wrap
    
    def get_first(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Get the highest priority extension instance."""
        with self._lock:
            extensions = self._extensions.get(name, [])
        if not extensions:
            raise KeyError(f"No extensions registered for '{name}'")
        return extensions[0].cls(*args, **kwargs)
    
    def get_all(self, name: str, *args: Any, **kwargs: Any) -> list[Any]:
        """Get instances of all registered extensions for a name."""
        with self._lock:
            extensions = self._extensions.get(name, [])
        return [ext.cls(*args, **kwargs) for ext in extensions]
    
    def get_classes(self, name: str) -> list[type]:
        """Get all registered classes for a name without instantiation."""
        with self._lock:
            extensions = self._extensions.get(name, [])
        return [ext.cls for ext in extensions]
    
    def get_infos(self, name: str) -> list[ExtensionInfo]:
        """Get all extension infos for a name."""
        with self._lock:
            return list(self._extensions.get(name, []))
    
    def has(self, name: str) -> bool:
        """Check if any extensions are registered for the given name."""
        with self._lock:
            return bool(self._extensions.get(name))
    
    def list_extension_points(self) -> list[str]:
        """Return a list of all registered extension points."""
        with self._lock:
            return list(self._extensions.keys())
    
    def count(self, name: str) -> int:
        """Count extensions registered for a name."""
        with self._lock:
            return len(self._extensions.get(name, []))
    
    def clear(self, name: str | None = None) -> None:
        """
        Clear registrations.
        
        Args:
            name: If provided, clear only this extension point.
                  If None, clear all registrations.
        """
        with self._lock:
            if name is None:
                self._extensions.clear()
            elif name in self._extensions:
                del self._extensions[name]


# ============================================================================
# Lazy Extension Manager
# ============================================================================


class LazyExtensionManager:
    """
    Extension manager with lazy module loading.
    
    Extensions are specified as 'module:class' strings and only loaded
    when accessed.
    
    Example:
        >>> LAZY = LazyExtensionManager("lazy")
        >>> LAZY.register_lazy("json", "json:JSONEncoder")
        >>> encoder = LAZY.load("json")  # Imports json module only now
    """
    
    def __init__(self, name: str = "default") -> None:
        self.name = name
        self._lazy_specs: dict[str, str] = {}
        self._loaded: dict[str, type] = {}
        self._lock = threading.RLock()
    
    def register_lazy(self, name: str, spec: str) -> None:
        """
        Register a lazy extension.
        
        Args:
            name: The name to register under.
            spec: The import spec in 'module:class' or 'module.submodule:class' format.
        """
        if ":" not in spec:
            raise ValueError(
                f"Invalid spec '{spec}'. Must be in 'module:class' format."
            )
        with self._lock:
            self._lazy_specs[name] = spec
            # Clear cached load if re-registering
            self._loaded.pop(name, None)
    
    def _import_class(self, spec: str) -> type:
        """Import a class from a module:class spec."""
        import importlib
        
        module_path, class_name = spec.rsplit(":", 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    
    def load(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Load and instantiate a lazily registered extension."""
        with self._lock:
            if name in self._loaded:
                cls = self._loaded[name]
            elif name in self._lazy_specs:
                cls = self._import_class(self._lazy_specs[name])
                self._loaded[name] = cls
            else:
                raise KeyError(f"Extension '{name}' not registered in {self.name}")
        return cls(*args, **kwargs)
    
    def get_class(self, name: str) -> type:
        """Get the class without instantiation (triggers import if needed)."""
        with self._lock:
            if name in self._loaded:
                return self._loaded[name]
            if name in self._lazy_specs:
                cls = self._import_class(self._lazy_specs[name])
                self._loaded[name] = cls
                return cls
            raise KeyError(f"Extension '{name}' not registered in {self.name}")
    
    def has(self, name: str) -> bool:
        """Check if an extension is registered."""
        with self._lock:
            return name in self._lazy_specs or name in self._loaded
    
    def is_loaded(self, name: str) -> bool:
        """Check if an extension has been loaded (imported)."""
        with self._lock:
            return name in self._loaded
    
    def list_registered(self) -> list[str]:
        """Return all registered extension names."""
        with self._lock:
            return list(set(self._lazy_specs.keys()) | set(self._loaded.keys()))


# ============================================================================
# Global Registry
# ============================================================================


class GlobalRegistry:
    """
    A singleton registry for managing multiple extension managers.
    
    Provides a centralized way to access all extension registries.
    """
    
    _instance: "GlobalRegistry | None" = None
    _lock = threading.Lock()
    
    def __new__(cls) -> "GlobalRegistry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._managers: dict[str, ExtensionManager] = {}
        return cls._instance
    
    def get_or_create(self, name: str) -> ExtensionManager:
        """Get or create an extension manager by name."""
        if name not in self._managers:
            self._managers[name] = ExtensionManager(name)
        return self._managers[name]
    
    def get(self, name: str) -> ExtensionManager | None:
        """Get an extension manager by name, or None if not found."""
        return self._managers.get(name)
    
    def list_managers(self) -> list[str]:
        """List all registered manager names."""
        return list(self._managers.keys())


# Global instance
_global_registry = GlobalRegistry()


def get_global_registry() -> GlobalRegistry:
    """Get the global extension registry."""
    return _global_registry


# ============================================================================
# Convenience Functions
# ============================================================================


def create_registry(name: str) -> ExtensionManager:
    """Create a new extension manager with the given name."""
    return ExtensionManager(name)


def create_typed_registry(name: str, base_class: type[_Base]) -> TypedExtensionManager[_Base]:
    """Create a new typed extension manager."""
    return TypedExtensionManager(name, base_class)


def create_multi_registry(name: str) -> MultiExtensionManager:
    """Create a new multi-extension manager."""
    return MultiExtensionManager(name)


def create_lazy_registry(name: str) -> LazyExtensionManager:
    """Create a new lazy extension manager."""
    return LazyExtensionManager(name)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Core classes
    "ExtensionManager",
    "TypedExtensionManager",
    "MultiExtensionManager",
    "LazyExtensionManager",
    "ExtensionInfo",
    "GlobalRegistry",
    # Factory functions
    "create_registry",
    "create_typed_registry", 
    "create_multi_registry",
    "create_lazy_registry",
    "get_global_registry",
]
