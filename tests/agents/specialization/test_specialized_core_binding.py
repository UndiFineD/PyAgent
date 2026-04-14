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

"""Core binding contract tests for specialization requests."""

from __future__ import annotations

import pytest

from src.agents.specialization.adapter_contracts import ShellExecutionRequest
from src.agents.specialization.errors import CoreBindingError
from src.agents.specialization.specialized_core_binding import SpecializedCoreBinding
from src.core.universal.UniversalCoreRegistry import UniversalCoreRegistry


class _Handler:
    """Test double core handler with async execute contract."""

    async def execute(self, envelope: object) -> dict[str, str]:
        """Execute a no-op handler for test resolution.

        Args:
            envelope: Envelope payload ignored by this test double.

        Returns:
            Deterministic payload marker.

        """
        _ = envelope
        return {"source": "core"}


def _request(core_target: str) -> ShellExecutionRequest:
    """Build shell request fixture.

    Args:
        core_target: Core target for binding.

    Returns:
        Canonical shell request fixture.

    """
    return ShellExecutionRequest(
        request_id="req-1",
        specialization_id="support",
        capability_action="summarize",
        core_target=core_target,
        policy_profile="default",
        correlation_id="corr-1",
    )


def test_plan_resolves_valid_core_target() -> None:
    """Binding planner should resolve valid core target contracts."""
    registry = UniversalCoreRegistry()
    registry.register("summarize", lambda: _Handler())

    plan = SpecializedCoreBinding(registry).plan(_request("summarize"))

    assert plan.core_target == "summarize"
    assert plan.handler is not None


def test_plan_rejects_unresolved_core_target() -> None:
    """Binding planner should fail closed for unresolved targets."""
    registry = UniversalCoreRegistry()

    with pytest.raises(CoreBindingError) as exc:
        SpecializedCoreBinding(registry).plan(_request("summarize"))

    assert exc.value.reason_code == "core_target_unresolved"
