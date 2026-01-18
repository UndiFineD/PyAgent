"""
Extension Registry Package - Phase 20
=====================================

Plugin system for managing extensible component registries.
"""

from .ExtensionRegistry import (
    ExtensionManager,
    TypedExtensionManager,
    MultiExtensionManager,
    LazyExtensionManager,
    ExtensionInfo,
    GlobalRegistry,
    create_registry,
    create_typed_registry,
    create_multi_registry,
    create_lazy_registry,
    get_global_registry,
)

__all__ = [
    "ExtensionManager",
    "TypedExtensionManager",
    "MultiExtensionManager",
    "LazyExtensionManager",
    "ExtensionInfo",
    "GlobalRegistry",
    "create_registry",
    "create_typed_registry",
    "create_multi_registry",
    "create_lazy_registry",
    "get_global_registry",
]
