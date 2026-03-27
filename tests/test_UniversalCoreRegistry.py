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

"""Red-phase contract tests for src/core/universal/UniversalCoreRegistry.py."""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass
from typing import Any

import pytest


def _import_or_fail(module_name: str) -> Any:
    """Import a module or fail with a red-phase behavioral message.

    Args:
        module_name: Fully-qualified module path to import.

    Returns:
        Imported module object.

    """
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.fail(
            (
                f"Missing implementation for registry behavior contract: {module_name}. "
                "This red-phase failure is expected before @6code implementation."
            ),
            pytrace=False,
        )


@dataclass
class _Handler:
    """Simple async handler used to validate registry contract behavior."""

    value: str

    async def execute(self, envelope: Any) -> dict[str, str]:
        """Return a deterministic payload used by tests.

        Args:
            envelope: Envelope payload forwarded by shell/registry contracts.

        Returns:
            Deterministic payload carrying the configured value.

        """
        _ = envelope
        return {"value": self.value}


def test_register_valid_factory_succeeds() -> None:
    """Register should accept a valid factory and expose the intent via has_intent."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    registry = registry_mod.UniversalCoreRegistry()

    registry.register("summarize", lambda: _Handler("ok"))

    assert registry.has_intent("summarize") is True


def test_register_duplicate_intent_raises_core_registration_error() -> None:
    """Register should reject duplicate intent registration in v1 contract."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    registry = registry_mod.UniversalCoreRegistry()

    registry.register("summarize", lambda: _Handler("first"))
    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.register("summarize", lambda: _Handler("second"))


def test_resolve_registered_intent_returns_handler_with_execute() -> None:
    """Resolve should return a handler exposing async execute per protocol contract."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    registry = registry_mod.UniversalCoreRegistry()
    registry.register("summarize", lambda: _Handler("ok"))

    handler = registry.resolve("summarize")

    assert hasattr(handler, "execute")
    assert inspect.iscoroutinefunction(handler.execute)


def test_resolve_missing_intent_raises_core_not_registered_error() -> None:
    """Resolve should raise CoreNotRegisteredError for missing intent values."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    registry = registry_mod.UniversalCoreRegistry()

    with pytest.raises(exc_mod.CoreNotRegisteredError):
        registry.resolve("missing")


def test_list_intents_returns_stable_tuple() -> None:
    """List should return stable tuple output across repeated calls."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    registry = registry_mod.UniversalCoreRegistry()
    registry.register("summarize", lambda: _Handler("ok"))
    registry.register("translate", lambda: _Handler("ok"))

    first = registry.list_intents()
    second = registry.list_intents()

    assert isinstance(first, tuple)
    assert isinstance(second, tuple)
    assert first == second
