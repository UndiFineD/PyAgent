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

"""Intent routing primitives and deterministic policy for the universal shell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from src.core.universal.exceptions import EnvelopeValidationError


@dataclass(frozen=True)
class TaskEnvelope:
    """Canonical task payload routed by the universal shell facade.

    Args:
        task_id: Stable task identifier for lineage and telemetry.
        intent: Requested capability label, optionally missing.
        payload: Structured task payload content.
        metadata: Non-secret contextual metadata for routing and tracing.

    """

    task_id: str
    intent: str | None
    payload: dict[str, Any]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RoutingDecision:
    """Result of intent normalization and route classification.

    Args:
        normalized_intent: Canonical normalized intent key.
        preferred_route: Chosen route name (`core` or `legacy`).
        reason: Deterministic explanation for the selected route.

    """

    normalized_intent: str
    preferred_route: Literal["core", "legacy"]
    reason: str


class UniversalIntentRouter:
    """Route intents to core or legacy handlers using allowlist policy."""

    def __init__(self, core_allowlist: set[str] | None = None) -> None:
        """Initialize the router.

        Args:
            core_allowlist: Set of intents eligible for direct core execution.

        """
        source_allowlist = core_allowlist or set()
        self._core_allowlist: frozenset[str] = frozenset(self.normalize_intent(intent) for intent in source_allowlist)

    def normalize_intent(self, intent: str | None) -> str:
        """Normalize an intent value to a deterministic canonical key.

        Args:
            intent: Raw intent value from the incoming envelope.

        Returns:
            Normalized lowercase intent, or `unknown` when unset/blank.

        """
        if intent is None:
            return "unknown"
        normalized = intent.strip().lower()
        if normalized == "":
            return "unknown"
        return normalized

    def classify(self, envelope: TaskEnvelope) -> RoutingDecision:
        """Classify a task envelope into a preferred execution route.

        Args:
            envelope: Valid task envelope to classify.

        Returns:
            RoutingDecision describing normalized intent and selected route.

        Raises:
            EnvelopeValidationError: If envelope is not a TaskEnvelope instance.

        """
        if not isinstance(envelope, TaskEnvelope):
            raise EnvelopeValidationError("Dispatch envelope must be a TaskEnvelope instance")

        normalized_intent = self.normalize_intent(envelope.intent)
        if normalized_intent in self._core_allowlist:
            return RoutingDecision(
                normalized_intent=normalized_intent,
                preferred_route="core",
                reason="allowlisted",
            )

        return RoutingDecision(
            normalized_intent=normalized_intent,
            preferred_route="legacy",
            reason="not_allowlisted",
        )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when the module contracts are importable and reachable.

    """
    return True


__all__ = ["TaskEnvelope", "RoutingDecision", "UniversalIntentRouter", "validate"]
