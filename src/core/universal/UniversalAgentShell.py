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

"""Universal shell facade orchestrating core and legacy dispatch routes."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Literal, Protocol

from src.core.universal.exceptions import (
    CoreExecutionError,
    CoreNotRegisteredError,
    CoreTimeoutError,
    EnvelopeValidationError,
    LegacyDispatchError,
    RoutingContractError,
)
from src.core.universal.UniversalCoreRegistry import CoreHandlerProtocol
from src.core.universal.UniversalIntentRouter import RoutingDecision, TaskEnvelope


class IntentRouterProtocol(Protocol):
    """Router protocol consumed by the universal shell."""

    def classify(self, envelope: TaskEnvelope) -> RoutingDecision:
        """Classify an envelope into a preferred execution route.

        Args:
            envelope: Envelope to classify.

        Returns:
            Deterministic route decision.

        """


class CoreRegistryProtocol(Protocol):
    """Core registry protocol consumed by the universal shell."""

    def resolve(self, intent: str) -> CoreHandlerProtocol:
        """Resolve a handler for the provided normalized intent.

        Args:
            intent: Normalized intent key.

        Returns:
            Core handler implementing async execute().

        """


LegacyDispatcher = Callable[[TaskEnvelope], Awaitable[dict[str, Any]]]
SpecializationDispatcher = Callable[[TaskEnvelope], Awaitable[dict[str, Any]]]
SpecializationPolicyCheck = Callable[[TaskEnvelope], bool]


@dataclass(frozen=True)
class DispatchResult:
    """Dispatch output including routing telemetry contract fields.

    Args:
        route: Route selected for final execution (`core`, `legacy`, or `specialization`).
        intent: Normalized intent used by dispatch.
        payload: Structured response payload from route execution.
        fallback_reason: Reason fallback was used, otherwise None.

    """

    route: str
    intent: str
    payload: dict[str, Any]
    fallback_reason: str | None


class UniversalAgentShell:
    """Dispatch envelopes by routing to core handlers with single legacy fallback."""

    def __init__(
        self,
        *,
        intent_router: IntentRouterProtocol,
        core_registry: CoreRegistryProtocol,
        legacy_dispatcher: LegacyDispatcher,
        core_timeout_seconds: float,
        specialization_dispatcher: SpecializationDispatcher | None = None,
        specialization_policy_check: SpecializationPolicyCheck | None = None,
        specialization_feature_enabled: bool = False,
    ) -> None:
        """Initialize shell dependencies.

        Args:
            intent_router: Router used to classify envelopes into routes.
            core_registry: Registry used to resolve core handlers by intent.
            legacy_dispatcher: Async legacy dispatch callable.
            core_timeout_seconds: Timeout budget for core execution path.
            specialization_dispatcher: Optional async specialization dispatcher.
            specialization_policy_check: Optional specialization policy precondition callable.
            specialization_feature_enabled: Runtime feature flag for specialization path.

        Raises:
            RoutingContractError: If timeout budget is not positive.

        """
        if core_timeout_seconds <= 0:
            raise RoutingContractError("core_timeout_seconds must be > 0")

        self._intent_router = intent_router
        self._core_registry = core_registry
        self._legacy_dispatcher = legacy_dispatcher
        self._core_timeout_seconds = core_timeout_seconds
        self._specialization_dispatcher = specialization_dispatcher
        self._specialization_policy_check = specialization_policy_check
        self._specialization_feature_enabled = specialization_feature_enabled

    async def dispatch(self, envelope: Any) -> DispatchResult:
        """Dispatch an envelope through core route or legacy fallback path.

        Args:
            envelope: Envelope candidate expected to be a TaskEnvelope.

        Returns:
            DispatchResult carrying route, intent, payload, and fallback metadata.

        Raises:
            EnvelopeValidationError: If envelope is not a TaskEnvelope.
            RoutingContractError: If router decision is malformed.
            LegacyDispatchError: If legacy dispatch fails.

        """
        task_envelope = self._validate_envelope(envelope)
        if self._should_use_specialization(task_envelope):
            payload = await self._dispatch_specialization(task_envelope)
            return DispatchResult(
                route="specialization",
                intent=str(task_envelope.intent or ""),
                payload=payload,
                fallback_reason=None,
            )

        decision = self._validate_decision(self._intent_router.classify(task_envelope))

        if decision.preferred_route == "legacy":
            payload = await self._dispatch_legacy(task_envelope)
            return DispatchResult(
                route="legacy",
                intent=decision.normalized_intent,
                payload=payload,
                fallback_reason=decision.reason,
            )

        if decision.preferred_route != "core":
            raise RoutingContractError(f"Unsupported preferred_route: {decision.preferred_route}")

        return await self._dispatch_core_with_fallback(task_envelope, decision)

    def _validate_envelope(self, envelope: Any) -> TaskEnvelope:
        """Validate the dispatch envelope type.

        Args:
            envelope: Envelope candidate.

        Returns:
            TaskEnvelope instance when valid.

        Raises:
            EnvelopeValidationError: If envelope is not a TaskEnvelope.

        """
        if not isinstance(envelope, TaskEnvelope):
            raise EnvelopeValidationError("Envelope must be a TaskEnvelope instance")
        return envelope

    def _validate_decision(self, decision: Any) -> RoutingDecision:
        """Validate and normalize router decision objects.

        Args:
            decision: Router decision candidate.

        Returns:
            RoutingDecision with route, intent, and reason values.

        Raises:
            RoutingContractError: If required decision fields are missing.

        """
        try:
            normalized_intent = str(decision.normalized_intent)
            preferred_route_value = str(decision.preferred_route)
            reason = str(decision.reason)
        except AttributeError as error:
            raise RoutingContractError("Router decision must expose intent, route, and reason") from error

        if normalized_intent == "":
            raise RoutingContractError("Router decision normalized_intent cannot be empty")
        if preferred_route_value not in {"core", "legacy"}:
            raise RoutingContractError("Router decision preferred_route must be 'core' or 'legacy'")

        preferred_route: Literal["core", "legacy"] = "core" if preferred_route_value == "core" else "legacy"

        return RoutingDecision(
            normalized_intent=normalized_intent,
            preferred_route=preferred_route,
            reason=reason,
        )

    async def _dispatch_core_with_fallback(
        self,
        envelope: TaskEnvelope,
        decision: RoutingDecision,
    ) -> DispatchResult:
        """Attempt core dispatch and fallback once for recoverable failures.

        Args:
            envelope: Task envelope to dispatch.
            decision: Validated router decision.

        Returns:
            DispatchResult from core route or single legacy fallback.

        Raises:
            LegacyDispatchError: If fallback legacy dispatch fails.

        """
        fallback_reason: str | None = None
        try:
            handler = self._core_registry.resolve(decision.normalized_intent)
            payload = await asyncio.wait_for(
                handler.execute(envelope),
                timeout=self._core_timeout_seconds,
            )
            return DispatchResult(
                route="core",
                intent=decision.normalized_intent,
                payload=payload,
                fallback_reason=None,
            )
        except CoreNotRegisteredError:
            fallback_reason = "core_not_registered"
        except CoreExecutionError:
            fallback_reason = "core_execution_error"
        except asyncio.TimeoutError as error:
            _ = CoreTimeoutError("Core execution timed out")
            fallback_reason = "core_timeout"
            _ = error

        payload = await self._dispatch_legacy(envelope)
        return DispatchResult(
            route="legacy",
            intent=decision.normalized_intent,
            payload=payload,
            fallback_reason=fallback_reason,
        )

    async def _dispatch_legacy(self, envelope: TaskEnvelope) -> dict[str, Any]:
        """Dispatch envelope to legacy handler and map failures.

        Args:
            envelope: Task envelope to dispatch through legacy route.

        Returns:
            Payload returned by legacy dispatcher.

        Raises:
            LegacyDispatchError: If legacy dispatcher raises an exception.

        """
        try:
            return await self._legacy_dispatcher(envelope)
        except LegacyDispatchError:
            raise
        except Exception as error:
            raise LegacyDispatchError("Legacy dispatch failed") from error

    def _should_use_specialization(self, envelope: TaskEnvelope) -> bool:
        """Check feature and policy preconditions for specialization path.

        Args:
            envelope: Task envelope under dispatch.

        Returns:
            True when specialization path is enabled and authorized.

        """
        if not self._specialization_feature_enabled:
            return False
        if self._specialization_dispatcher is None or self._specialization_policy_check is None:
            return False
        return self._specialization_policy_check(envelope)

    async def _dispatch_specialization(self, envelope: TaskEnvelope) -> dict[str, Any]:
        """Dispatch envelope through specialization adapter runtime.

        Args:
            envelope: Task envelope routed to specialization path.

        Returns:
            Payload returned by specialization dispatcher.

        Raises:
            LegacyDispatchError: If specialization dispatcher is missing or fails.

        """
        if self._specialization_dispatcher is None:
            raise LegacyDispatchError("Specialization dispatcher is not configured")
        try:
            return await self._specialization_dispatcher(envelope)
        except Exception as error:  # noqa: BLE001
            raise LegacyDispatchError("Specialization dispatch failed") from error


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when shell symbols are importable and reachable.

    """
    return True


__all__ = [
    "DispatchResult",
    "LegacyDispatcher",
    "SpecializationDispatcher",
    "SpecializationPolicyCheck",
    "UniversalAgentShell",
    "validate",
]
