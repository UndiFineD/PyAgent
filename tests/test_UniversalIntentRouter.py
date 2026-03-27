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

"""Red-phase contract tests for src/core/universal/UniversalIntentRouter.py."""

from __future__ import annotations

import importlib
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
                f"Missing implementation for router behavior contract: {module_name}. "
                "This red-phase failure is expected before @6code implementation."
            ),
            pytrace=False,
        )


def _make_envelope(router_mod: Any, *, intent: str | None) -> Any:
    """Create a canonical task envelope for router contract tests.

    Args:
        router_mod: Imported router module exposing TaskEnvelope.
        intent: Intent value to test normalization/classification behavior.

    Returns:
        TaskEnvelope instance.

    """
    return router_mod.TaskEnvelope(
        task_id="task-router-1",
        intent=intent,
        payload={"value": 1},
        metadata={"source": "unit-test"},
    )


def test_normalize_intent_lowercases_known_value() -> None:
    """Normalize should lowercase and trim a known intent value."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"summarize"})

    normalized = router.normalize_intent("  SuMMarize  ")
    assert normalized == "summarize"


def test_normalize_intent_none_returns_unknown() -> None:
    """Normalize should map missing intent values to the unknown sentinel."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"summarize"})

    assert router.normalize_intent(None) == "unknown"
    assert router.normalize_intent("") == "unknown"


def test_classify_allowlisted_intent_prefers_core() -> None:
    """Classify should choose core route for allowlisted normalized intents."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"summarize"})
    envelope = _make_envelope(router_mod, intent="Summarize")

    decision = router.classify(envelope)
    assert decision.normalized_intent == "summarize"
    assert decision.preferred_route == "core"


def test_classify_non_allowlisted_intent_prefers_legacy() -> None:
    """Classify should choose legacy route for non-allowlisted intents."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"summarize"})
    envelope = _make_envelope(router_mod, intent="translate")

    decision = router.classify(envelope)
    assert decision.normalized_intent == "translate"
    assert decision.preferred_route == "legacy"


def test_classify_is_deterministic_for_identical_envelope() -> None:
    """Classify should return equivalent decisions for equivalent envelopes."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"summarize"})
    first = _make_envelope(router_mod, intent="Summarize")
    second = _make_envelope(router_mod, intent="Summarize")

    first_decision = router.classify(first)
    second_decision = router.classify(second)

    assert first_decision.normalized_intent == second_decision.normalized_intent
    assert first_decision.preferred_route == second_decision.preferred_route
    assert first_decision.reason == second_decision.reason
