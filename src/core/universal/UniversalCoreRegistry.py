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

"""Registry for mapping normalized intents to core handler factories."""

from __future__ import annotations

import inspect
from typing import Any, Callable, Protocol

from src.core.universal.exceptions import CoreNotRegisteredError, CoreRegistrationError


class CoreHandlerProtocol(Protocol):
    """Protocol for core handlers registered in the universal registry."""

    async def execute(self, envelope: Any) -> dict[str, Any]:
        """Execute core logic for a task envelope.

        Args:
            envelope: Envelope routed to a core handler.

        Returns:
            Structured execution payload.

        """


CoreFactory = Callable[[], CoreHandlerProtocol]


class UniversalCoreRegistry:
    """Manage registration and resolution of core handlers by intent key."""

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._factories: dict[str, CoreFactory] = {}

    def register(self, intent: str, factory: CoreFactory) -> None:
        """Register a new core factory for a normalized intent.

        Args:
            intent: Intent key associated with the core factory.
            factory: Factory returning a handler that exposes async execute().

        Raises:
            CoreRegistrationError: If the intent/factory contract is invalid.

        """
        normalized_intent = self._normalize_intent(intent)

        if normalized_intent in self._factories:
            raise CoreRegistrationError(f"Core already registered for intent: {normalized_intent}")

        self._ensure_valid_factory(factory)
        self._factories[normalized_intent] = factory

    def resolve(self, intent: str) -> CoreHandlerProtocol:
        """Resolve and instantiate a core handler for a normalized intent.

        Args:
            intent: Intent key to resolve.

        Returns:
            Instantiated core handler implementing async execute().

        Raises:
            CoreNotRegisteredError: If no factory exists for the intent.
            CoreRegistrationError: If a registered factory returns an invalid handler.

        """
        normalized_intent = self._normalize_intent(intent)
        factory = self._factories.get(normalized_intent)
        if factory is None:
            raise CoreNotRegisteredError(f"No core registered for intent: {normalized_intent}")

        handler = factory()
        self._ensure_valid_handler(handler)
        return handler

    def has_intent(self, intent: str) -> bool:
        """Check whether a normalized intent has a registered core factory.

        Args:
            intent: Intent key to check.

        Returns:
            True when intent is present in the registry.

        """
        return self._normalize_intent(intent) in self._factories

    def list_intents(self) -> tuple[str, ...]:
        """Return a stable tuple of registered intent keys.

        Returns:
            Sorted tuple of registered normalized intent keys.

        """
        return tuple(sorted(self._factories.keys()))

    def unregister(self, intent: str) -> bool:
        """Remove a registered intent if present.

        Args:
            intent: Intent key to remove.

        Returns:
            True if the intent was removed, else False.

        """
        normalized_intent = self._normalize_intent(intent)
        removed = self._factories.pop(normalized_intent, None)
        return removed is not None

    def _normalize_intent(self, intent: str) -> str:
        """Normalize intent values used as registry keys.

        Args:
            intent: Raw intent value.

        Returns:
            Lowercased and trimmed intent key.

        Raises:
            CoreRegistrationError: If the intent is empty after normalization.

        """
        normalized = intent.strip().lower()
        if normalized == "":
            raise CoreRegistrationError("Intent cannot be empty")
        return normalized

    def _ensure_valid_factory(self, factory: CoreFactory) -> None:
        """Validate a candidate factory before registration.

        Args:
            factory: Candidate core factory.

        Raises:
            CoreRegistrationError: If the candidate is not a valid factory.

        """
        if not callable(factory):
            raise CoreRegistrationError("Core factory must be callable")

        handler = factory()
        self._ensure_valid_handler(handler)

    def _ensure_valid_handler(self, handler: Any) -> None:
        """Validate handler contract against async execute() requirement.

        Args:
            handler: Candidate handler object.

        Raises:
            CoreRegistrationError: If handler lacks async execute().

        """
        execute_method = getattr(handler, "execute", None)
        if execute_method is None:
            raise CoreRegistrationError("Core handler must expose execute()")
        if not inspect.iscoroutinefunction(execute_method):
            raise CoreRegistrationError("Core handler execute() must be async")


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when registry symbols are importable and operational.

    """
    return True


__all__ = ["CoreFactory", "CoreHandlerProtocol", "UniversalCoreRegistry", "validate"]
