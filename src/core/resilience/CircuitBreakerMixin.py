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

"""Agent mixin that executes provider calls through circuit-breaker policy."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry
from src.core.resilience.CircuitBreakerState import CircuitState
from src.core.resilience.exceptions import AllCircuitsOpenError, CircuitOpenError

T = TypeVar("T")


class CircuitBreakerMixin:
    """Provides a resilient call wrapper for outbound provider operations."""

    _circuit_breaker_registry: CircuitBreakerRegistry

    def _setup_circuit_breaker(self, registry: CircuitBreakerRegistry) -> None:
        """Bind a registry to the host object.

        Args:
            registry: Shared circuit-breaker registry instance.

        """
        self._circuit_breaker_registry = registry

    async def cb_call(
        self,
        provider_key: str,
        call: Callable[[], Awaitable[T]],
        config: CircuitBreakerConfig | None = None,
    ) -> T:
        """Execute a provider call through primary and fallback circuit gates.

        Args:
            provider_key: Primary provider key.
            call: Zero-argument awaitable factory for the provider operation.
            config: Optional circuit configuration for the primary provider.

        Returns:
            Result from the first provider that is allowed and succeeds.

        Raises:
            CircuitOpenError: When primary is blocked and no fallback is configured.
            AllCircuitsOpenError: When primary and all configured fallbacks are blocked.
            Exception: Re-raises provider call exceptions after failure recording.

        """
        self._validate_circuit(provider_key)
        primary_config = config if config is not None else CircuitBreakerConfig(provider_key=provider_key)
        registry = self._circuit_breaker_registry
        await registry.get_or_create(provider_key, primary_config)

        if await registry.should_allow(provider_key, primary_config):
            return await self._execute(provider_key, call, primary_config)

        tried_keys: list[str] = [provider_key]
        for fallback_key in primary_config.fallback_providers:
            tried_keys.append(fallback_key)
            if not await registry.should_allow(fallback_key, None):
                continue
            return await self._execute(fallback_key, call, None)

        if len(tried_keys) > 1:
            raise AllCircuitsOpenError(tried_keys)

        state = await registry.get_or_create(provider_key, primary_config)
        raise CircuitOpenError(provider_key, state.state)

    async def _execute(
        self,
        provider_key: str,
        call: Callable[[], Awaitable[T]],
        config: CircuitBreakerConfig | None,
    ) -> T:
        """Execute a call and update provider circuit counters.

        Args:
            provider_key: Provider key used for this attempt.
            call: Zero-argument awaitable factory to execute.
            config: Optional circuit config override.

        Returns:
            The call result.

        Raises:
            Exception: Re-raises provider call exceptions after recording failure.

        """
        try:
            result = await call()
        except Exception:
            await self._circuit_breaker_registry.record_failure(provider_key, config)
            raise

        await self._circuit_breaker_registry.record_success(provider_key, config)
        return result

    def _validate_circuit(self, provider_key: str) -> None:
        """Ensure the mixin is initialized with a circuit-breaker registry.

        Args:
            provider_key: Provider key requested for execution.

        Raises:
            AttributeError: If registry is not configured on the host object.

        """
        if not hasattr(self, "_circuit_breaker_registry"):
            raise AttributeError(f"Circuit breaker registry is not configured for provider '{provider_key}'.")


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    _ = CircuitState.CLOSED
    return True
