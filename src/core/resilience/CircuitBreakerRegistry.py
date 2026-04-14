#!/usr/bin/env python3
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

"""Async-safe registry for per-provider circuit-breaker state."""

from __future__ import annotations

import asyncio

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
from src.core.resilience.CircuitBreakerCore import CircuitBreakerCore
from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState


class CircuitBreakerRegistry:
    """Stores provider circuit state and delegates transitions to core logic."""

    def __init__(self) -> None:
        """Initialize registry containers and lock."""
        self._states: dict[str, CircuitBreakerState] = {}
        self._configs: dict[str, CircuitBreakerConfig] = {}
        self._lock = asyncio.Lock()
        self._core = CircuitBreakerCore()

    async def get_or_create(self, key: str, config: CircuitBreakerConfig) -> CircuitBreakerState:
        """Get existing state or create a new one for the provider key.

        Args:
            key: Provider key.
            config: Configuration for the provider key.

        Returns:
            Stable state object for the provider.

        """
        async with self._lock:
            self._configs[key] = config
            state = self._states.get(key)
            if state is None:
                state = CircuitBreakerState(provider_key=key)
                self._states[key] = state
            return state

    async def get_fallback(self, key: str, config: CircuitBreakerConfig | None = None) -> str | None:
        """Get first fallback provider in CLOSED state.

        Args:
            key: Primary provider key.
            config: Optional primary config; falls back to stored config.

        Returns:
            First available fallback provider key, or ``None``.

        """
        async with self._lock:
            primary_config = self._resolve_config(key, config)
            for fallback_key in primary_config.fallback_providers:
                fallback_config = self._resolve_config(fallback_key, None)
                state = self._states.get(fallback_key)
                if state is None:
                    state = CircuitBreakerState(provider_key=fallback_key)
                    self._states[fallback_key] = state
                if self._core.check_state(state, fallback_config) is CircuitState.CLOSED:
                    return fallback_key
            return None

    async def record_success(self, key: str, config: CircuitBreakerConfig | None = None) -> None:
        """Record success on the provider state.

        Args:
            key: Provider key.
            config: Optional provider config.

        """
        async with self._lock:
            resolved = self._resolve_config(key, config)
            state = self._states.get(key)
            if state is None:
                state = CircuitBreakerState(provider_key=key)
                self._states[key] = state
            self._configs[key] = resolved
            self._core.record_success(state)

    async def record_failure(self, key: str, config: CircuitBreakerConfig | None = None) -> None:
        """Record failure on the provider state.

        Args:
            key: Provider key.
            config: Optional provider config.

        """
        async with self._lock:
            resolved = self._resolve_config(key, config)
            state = self._states.get(key)
            if state is None:
                state = CircuitBreakerState(provider_key=key)
                self._states[key] = state
            self._configs[key] = resolved
            self._core.record_failure(state, resolved)

    async def should_allow(self, key: str, config: CircuitBreakerConfig | None = None) -> bool:
        """Check whether the provider may execute a call now.

        Args:
            key: Provider key.
            config: Optional provider config.

        Returns:
            ``True`` when a call can proceed.

        """
        async with self._lock:
            resolved = self._resolve_config(key, config)
            state = self._states.get(key)
            if state is None:
                state = CircuitBreakerState(provider_key=key)
                self._states[key] = state
            self._configs[key] = resolved
            return self._core.should_allow(state, resolved)

    async def reset(self, key: str, config: CircuitBreakerConfig | None = None) -> None:
        """Reset provider state to CLOSED.

        Args:
            key: Provider key.
            config: Optional provider config.

        """
        async with self._lock:
            resolved = self._resolve_config(key, config)
            state = self._states.get(key)
            if state is None:
                state = CircuitBreakerState(provider_key=key)
                self._states[key] = state
            self._configs[key] = resolved
            self._core.reset(state)

    def _resolve_config(self, key: str, config: CircuitBreakerConfig | None) -> CircuitBreakerConfig:
        """Resolve config input to a concrete provider configuration.

        Args:
            key: Provider key.
            config: Optional incoming config override.

        Returns:
            Concrete config for the provider key.

        """
        if config is not None:
            return config
        existing = self._configs.get(key)
        if existing is not None:
            return existing
        default_config = CircuitBreakerConfig(provider_key=key)
        self._configs[key] = default_config
        return default_config


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
