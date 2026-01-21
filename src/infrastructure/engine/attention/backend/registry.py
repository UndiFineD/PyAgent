# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Registry for attention backends with capability-based selection.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from .base import AttentionBackend
from .models import AttentionBackendEnum, AttentionCapabilities, AttentionType
from .naive import NaiveAttentionBackend
from .sdpa import TorchSDPABackend, HAS_TORCH, torch
from .flash import FlashAttentionBackend
from .flashinfer import FlashInferBackend
from .packkv import PackKVAttentionBackend

logger = logging.getLogger(__name__)


class AttentionBackendRegistry:
    """
    Registry for attention backends with capability-based selection.

    Features:
    - Backend registration and discovery
    - Capability-based lookup
    - Runtime hot-swap (beyond vLLM)
    - Fallback chains
    """

    _instance: AttentionBackendRegistry | None = None

    def __new__(cls) -> AttentionBackendRegistry:
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_registry()
        return cls._instance

    def _init_registry(self) -> None:
        """Initialize the registry with default backends."""
        self._backends: dict[str, type[AttentionBackend]] = {}
        self._active_backend: AttentionBackend | None = None
        self._fallback_chain: list[str] = []
        self._hot_swap_enabled: bool = True

        # Register default backends
        self.register(NaiveAttentionBackend)
        self.register(TorchSDPABackend)
        self.register(FlashAttentionBackend)
        self.register(FlashInferBackend)
        self.register(PackKVAttentionBackend)

        # Default fallback chain
        self._fallback_chain = [
            "packkv",
            "flash_attn",
            "flashinfer",
            "torch_sdpa",
            "naive",
        ]

    def register(
        self,
        backend_cls: type[AttentionBackend],
        override: bool = False,
    ) -> None:
        """
        Register an attention backend.

        Args:
            backend_cls: Backend class to register
            override: Whether to override existing registration
        """
        name = backend_cls.get_name()

        if name in self._backends and not override:
            logger.warning(f"Backend '{name}' already registered, skipping")
            return

        self._backends[name] = backend_cls
        logger.debug(f"Registered attention backend: {name}")

    def unregister(self, name: str) -> bool:
        """
        Unregister a backend.

        Args:
            name: Backend name to remove

        Returns:
            True if removed, False if not found
        """
        if name in self._backends:
            del self._backends[name]
            if name in self._fallback_chain:
                self._fallback_chain.remove(name)
            logger.debug(f"Unregistered attention backend: {name}")
            return True
        return False

    def get_backend(
        self,
        name: str | AttentionBackendEnum | None = None,
    ) -> AttentionBackend | None:
        """
        Get a backend by name.

        Args:
            name: Backend name or enum (uses active if None)

        Returns:
            Backend instance or None
        """
        if name is None:
            return self._active_backend

        if isinstance(name, AttentionBackendEnum):
            name = name.value

        backend_cls = self._backends.get(name)
        if backend_cls is not None:
            return backend_cls()
        return None

    def select_backend(
        self,
        capabilities: AttentionCapabilities | None = None,
        attn_type: AttentionType | None = None,
        prefer: str | None = None,
    ) -> AttentionBackend | None:
        """
        Select best backend based on requirements.

        Args:
            capabilities: Required capabilities
            attn_type: Required attention type
            prefer: Preferred backend name

        Returns:
            Best matching backend
        """
        # Try preferred first
        if prefer:
            backend = self.get_backend(prefer)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend

        # Try fallback chain
        for name in self._fallback_chain:
            backend = self.get_backend(name)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend

        # Try any backend
        for name in self._backends:
            backend = self.get_backend(name)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend

        return None

    def _check_backend(
        self,
        backend: AttentionBackend,
        capabilities: AttentionCapabilities | None,
        attn_type: AttentionType | None,
    ) -> bool:
        """Check if backend meets requirements."""
        if attn_type is not None and not backend.supports(attn_type):
            return False

        if capabilities is not None:
            caps = backend.get_capabilities()
            # Check key capabilities
            if capabilities.supports_sliding_window and not caps.supports_sliding_window:
                return False
            if capabilities.supports_fp8 and not caps.supports_fp8:
                return False
            if capabilities.requires_cuda and not caps.requires_cuda:
                return False

        return True

    def set_active(
        self,
        backend: str | AttentionBackend | AttentionBackendEnum,
    ) -> bool:
        """
        Set the active backend.

        Args:
            backend: Backend name, instance, or enum

        Returns:
            True if set successfully
        """
        if isinstance(backend, str):
            self._active_backend = self.get_backend(backend)
        elif isinstance(backend, AttentionBackendEnum):
            self._active_backend = self.get_backend(backend.value)
        else:
            self._active_backend = backend

        if self._active_backend:
            logger.info(f"Active attention backend: {self._active_backend.get_name()}")
            return True
        return False

    def hot_swap(
        self,
        new_backend: str | AttentionBackend,
    ) -> bool:
        """
        Hot-swap to a new backend without restart.

        Beyond vLLM: Allows runtime backend changes.

        Args:
            new_backend: New backend to use

        Returns:
            True if swap successful
        """
        if not self._hot_swap_enabled:
            logger.warning("Hot-swap disabled")
            return False

        old_backend = self._active_backend

        if self.set_active(new_backend):
            if old_backend:
                logger.info(
                    f"Hot-swapped from {old_backend.get_name()} to "
                    f"{self._active_backend.get_name()}"  # type: ignore
                )
            return True

        # Restore on failure
        self._active_backend = old_backend
        return False

    def set_fallback_chain(self, chain: list[str]) -> None:
        """Set the backend fallback chain."""
        self._fallback_chain = chain

    def list_backends(self) -> list[str]:
        """List all registered backends."""
        return list(self._backends.keys())

    def get_capabilities(self, name: str) -> AttentionCapabilities | None:
        """Get capabilities for a backend."""
        backend_cls = self._backends.get(name)
        if backend_cls:
            return backend_cls.get_capabilities()
        return None

    @lru_cache(maxsize=32)
    def _check_availability(self, name: str) -> bool:
        """Check if backend is actually usable."""
        backend = self.get_backend(name)
        if backend is None:
            return False

        caps = backend.get_capabilities()

        # Check CUDA requirement
        if caps.requires_cuda and (not HAS_TORCH or not torch.cuda.is_available()):
            return False

        # Check SM version
        if HAS_TORCH and torch.cuda.is_available():
            major, minor = torch.cuda.get_device_capability()
            sm_version = major * 10 + minor
            if sm_version < caps.min_sm_version:
                return False

        return True

    def get_available_backends(self) -> list[str]:
        """Get list of actually usable backends."""
        return [name for name in self._backends if self._check_availability(name)]


# Convenience function
def get_attention_registry() -> AttentionBackendRegistry:
    """Get the singleton attention backend registry."""
    return AttentionBackendRegistry()
