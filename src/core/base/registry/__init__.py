#!/usr/bin/env python3
from __future__ import annotations
"""
Extension Registry Package

Plugin system for managing extensible component registries.
"""




try:
    from .extension_registry import (
        ExtensionInfo,
        ExtensionManager,
        TypedExtensionManager,
        MultiExtensionManager,
        LazyExtensionManager,
        GlobalRegistry,
        create_registry,
        create_typed_registry,
        create_multi_registry,
        create_lazy_registry,
        get_global_registry,
    )
except Exception:
    # Fallback absolute import for non-package execution contexts
    from src.core.base.extension_registry import (
        ExtensionInfo,
        ExtensionManager,
        TypedExtensionManager,
        MultiExtensionManager,
        LazyExtensionManager,
        GlobalRegistry,
        create_registry,
        create_typed_registry,
        create_multi_registry,
        create_lazy_registry,
        get_global_registry,
    )

__all__ = [
    "ExtensionInfo",
    "ExtensionManager",
    "TypedExtensionManager",
    "MultiExtensionManager",
    "LazyExtensionManager",
    "GlobalRegistry",
    "create_registry",
    "create_typed_registry",
    "create_multi_registry",
    "create_lazy_registry",
    "get_global_registry",
]
