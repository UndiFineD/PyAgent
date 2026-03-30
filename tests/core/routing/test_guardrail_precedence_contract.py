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

"""Contract tests for deterministic guardrail precedence."""

from __future__ import annotations

import pytest

from src.core.routing.prompt_routing_facade import PromptRoutingFacade
from src.core.routing.routing_models import PromptRoutingRequest


@pytest.mark.asyncio
async def test_guardrail_precedence_overrides_classifier_candidates() -> None:
    """Guardrails must finalize route before classifier and tie-break stages."""
    facade = PromptRoutingFacade(policy={"policy_version": "spr-v1", "confidence_threshold": 0.99})
    request = PromptRoutingRequest(
        request_id="req-guardrail-1",
        tenant_id="tenant-1",
        intent_hint="analyze",
        risk_class="high",
        tool_requirement=None,
        latency_budget_ms=30,
        cost_budget_class="normal",
        context_summary="safe context",
    )

    record = await facade.route(request)
    assert record.decision_stage == "guardrail"
    assert record.final_route == "safe_default"
    assert record.guardrail_hit is True
