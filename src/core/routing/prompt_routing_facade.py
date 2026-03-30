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

"""Facade that orchestrates smart prompt routing stages."""

from __future__ import annotations

import uuid

from src.core.routing.classifier_schema import ClassifierSchemaError, validate_classifier_result
from src.core.routing.confidence_calibration import calibrate_confidence
from src.core.routing.fallback_reason_taxonomy import (
    CLASSIFIER_PROVIDER_ERROR,
    SCHEMA_VALIDATION_FAILED,
    TIE_BREAK_TIMEOUT,
    TIE_BREAK_UNRESOLVED,
)
from src.core.routing.guardrail_policy_engine import GuardrailPolicyEngine
from src.core.routing.policy_versioning import resolve_policy_version
from src.core.routing.prompt_semantic_classifier import PromptSemanticClassifier
from src.core.routing.request_normalizer import normalize_request
from src.core.routing.routing_fallback_policy import RoutingFallbackPolicy
from src.core.routing.routing_models import PromptRoutingRequest, RouteDecisionRecord
from src.core.routing.routing_policy_loader import load_policy
from src.core.routing.routing_telemetry_emitter import RoutingTelemetryEmitter
from src.core.routing.tie_break_resolver import TieBreakResolver, TieBreakTimeoutError


class PromptRoutingFacade:
    """Async entrypoint implementing guardrail-first hybrid routing."""

    def __init__(
        self,
        *,
        guardrail_engine: GuardrailPolicyEngine | None = None,
        classifier: PromptSemanticClassifier | None = None,
        tie_break_resolver: TieBreakResolver | None = None,
        fallback_policy: RoutingFallbackPolicy | None = None,
        telemetry_emitter: RoutingTelemetryEmitter | None = None,
        policy: dict[str, object] | None = None,
    ) -> None:
        """Initialize routing facade dependencies.

        Args:
            guardrail_engine: Guardrail engine implementation.
            classifier: Semantic classifier implementation.
            tie_break_resolver: Tie-break resolver implementation.
            fallback_policy: Fallback policy implementation.
            telemetry_emitter: Telemetry emitter implementation.
            policy: Optional policy map override.

        """
        self._guardrail_engine = guardrail_engine or GuardrailPolicyEngine()
        self._classifier = classifier or PromptSemanticClassifier()
        self._tie_break_resolver = tie_break_resolver or TieBreakResolver()
        self._fallback_policy = fallback_policy or RoutingFallbackPolicy()
        self._telemetry_emitter = telemetry_emitter or RoutingTelemetryEmitter()
        self._policy = load_policy(policy)

    async def route(self, request: PromptRoutingRequest) -> RouteDecisionRecord:
        """Route one request and always return decision or fail-closed fallback.

        Args:
            request: Routing request.

        Returns:
            Final routing decision record.

        """
        normalized = normalize_request(request)
        policy_version = resolve_policy_version(self._policy)
        correlation_id = f"spr-{uuid.uuid4()}"

        guardrail = self._guardrail_engine.evaluate(normalized)
        if guardrail.is_resolved and guardrail.route is not None:
            record = RouteDecisionRecord(
                request_id=normalized.request_id,
                final_route=guardrail.route,
                decision_stage="guardrail",
                guardrail_hit=True,
                classifier_confidence=0.0,
                tie_break_used=False,
                fallback_reason=guardrail.deny_reason,
                policy_version=policy_version,
                correlation_id=correlation_id,
            )
            self._telemetry_emitter.emit(request=normalized, record=record)
            return record

        try:
            classification = self._classifier.classify(normalized)
            validate_classifier_result(classification)
            confidence = calibrate_confidence(classification.confidence)
            threshold = float(self._policy.get("confidence_threshold", 0.75))

            if confidence >= threshold:
                chosen = classification.candidate_routes[0]
                record = RouteDecisionRecord(
                    request_id=normalized.request_id,
                    final_route=chosen.route,
                    decision_stage="classifier",
                    guardrail_hit=False,
                    classifier_confidence=confidence,
                    tie_break_used=False,
                    fallback_reason=None,
                    policy_version=policy_version,
                    correlation_id=correlation_id,
                )
                self._telemetry_emitter.emit(request=normalized, record=record)
                return record

            tie_break_timeout_ms = int(self._policy.get("tie_break_timeout_ms", 20))
            tie_break_choice = self._tie_break_resolver.resolve(
                classification.candidate_routes,
                timeout_ms=tie_break_timeout_ms,
                seed=normalized.request_id,
            )
            if tie_break_choice is None:
                return self._fallback_policy.apply(
                    reason=TIE_BREAK_UNRESOLVED,
                    request=normalized,
                    policy_version=policy_version,
                    correlation_id=correlation_id,
                )

            record = RouteDecisionRecord(
                request_id=normalized.request_id,
                final_route=tie_break_choice.route,
                decision_stage="tie_break",
                guardrail_hit=False,
                classifier_confidence=confidence,
                tie_break_used=True,
                fallback_reason=None,
                policy_version=policy_version,
                correlation_id=correlation_id,
            )
            self._telemetry_emitter.emit(request=normalized, record=record)
            return record
        except ClassifierSchemaError:
            return self._fallback_policy.apply(
                reason=SCHEMA_VALIDATION_FAILED,
                request=normalized,
                policy_version=policy_version,
                correlation_id=correlation_id,
            )
        except TieBreakTimeoutError:
            return self._fallback_policy.apply(
                reason=TIE_BREAK_TIMEOUT,
                request=normalized,
                policy_version=policy_version,
                correlation_id=correlation_id,
            )
        except Exception:
            return self._fallback_policy.apply(
                reason=CLASSIFIER_PROVIDER_ERROR,
                request=normalized,
                policy_version=policy_version,
                correlation_id=correlation_id,
            )
