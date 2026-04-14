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

"""Request normalization helpers for routing facade input."""

from __future__ import annotations

from src.core.routing.routing_models import PromptRoutingRequest


def normalize_request(request: PromptRoutingRequest) -> PromptRoutingRequest:
    """Normalize incoming request with bounded context summary.

    Args:
        request: Input request.

    Returns:
        Normalized request preserving deterministic semantics.

    """
    bounded_summary = request.context_summary.strip()[:256]
    bounded_intent = None if request.intent_hint is None else request.intent_hint.strip()

    return PromptRoutingRequest(
        request_id=request.request_id,
        tenant_id=request.tenant_id,
        intent_hint=bounded_intent,
        risk_class=request.risk_class.strip().lower(),
        tool_requirement=request.tool_requirement,
        latency_budget_ms=request.latency_budget_ms,
        cost_budget_class=request.cost_budget_class.strip().lower(),
        context_summary=bounded_summary,
    )


def validate() -> bool:
    """Validate deterministic request normalization behavior.

    Returns:
        True when normalization trims and bounds request fields.

    """
    normalized = normalize_request(
        PromptRoutingRequest(
            request_id="validate-normalizer",
            tenant_id="tenant",
            intent_hint="  intent  ",
            risk_class=" HIGH ",
            tool_requirement=None,
            latency_budget_ms=100,
            cost_budget_class=" STANDARD ",
            context_summary="x" * 400,
        )
    )
    return (
        normalized.risk_class == "high"
        and normalized.cost_budget_class == "standard"
        and len(normalized.context_summary) == 256
    )
