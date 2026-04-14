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

"""Feature-flag tests for specialization route in universal shell."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import pytest

from src.core.universal.UniversalAgentShell import UniversalAgentShell
from src.core.universal.UniversalIntentRouter import TaskEnvelope


@dataclass
class _Decision:
    """Router decision value object for test routes."""

    normalized_intent: str
    preferred_route: str
    reason: str


class _Router:
    """Deterministic router test double."""

    def classify(self, envelope: TaskEnvelope) -> _Decision:
        """Classify all envelopes to core route.

        Args:
            envelope: Task envelope under dispatch.

        Returns:
            Deterministic route decision.

        """
        _ = envelope
        return _Decision(normalized_intent="summarize", preferred_route="core", reason="allowlisted")


class _Handler:
    """Core handler test double."""

    async def execute(self, envelope: TaskEnvelope) -> dict[str, str]:
        """Execute core path test behavior.

        Args:
            envelope: Task envelope under dispatch.

        Returns:
            Core payload marker.

        """
        _ = envelope
        return {"source": "core"}


class _Registry:
    """Core registry test double."""

    def has_intent(self, intent: str) -> bool:
        """Check intent presence in test registry.

        Args:
            intent: Intent value.

        Returns:
            Always True for this test double.

        """
        _ = intent
        return True

    def resolve(self, intent: str) -> _Handler:
        """Resolve deterministic handler.

        Args:
            intent: Intent value.

        Returns:
            Handler test double.

        """
        _ = intent
        return _Handler()


@pytest.mark.asyncio
async def test_specialization_path_runs_when_flag_and_policy_are_enabled() -> None:
    """Specialization path should run only when both preconditions are true."""

    async def specialization_dispatcher(envelope: TaskEnvelope) -> dict[str, str]:
        """Return specialization payload marker.

        Args:
            envelope: Task envelope under dispatch.

        Returns:
            Specialization payload marker.

        """
        _ = envelope
        await asyncio.sleep(0)
        return {"source": "specialization"}

    shell = UniversalAgentShell(
        intent_router=_Router(),
        core_registry=_Registry(),
        legacy_dispatcher=lambda envelope: asyncio.sleep(0, result={"source": "legacy"}),
        core_timeout_seconds=0.1,
        specialization_dispatcher=specialization_dispatcher,
        specialization_policy_check=lambda envelope: bool(envelope.intent),
        specialization_feature_enabled=True,
    )

    result = await shell.dispatch(
        TaskEnvelope(
            task_id="task-1",
            intent="summarize",
            payload={"message": "hello"},
            metadata={},
        )
    )

    assert result.route == "specialization"
    assert result.payload == {"source": "specialization"}


@pytest.mark.asyncio
async def test_specialization_path_is_skipped_when_flag_is_disabled() -> None:
    """Disabled feature flag should preserve baseline core route behavior."""
    shell = UniversalAgentShell(
        intent_router=_Router(),
        core_registry=_Registry(),
        legacy_dispatcher=lambda envelope: asyncio.sleep(0, result={"source": "legacy"}),
        core_timeout_seconds=0.1,
        specialization_dispatcher=lambda envelope: asyncio.sleep(0, result={"source": "specialization"}),
        specialization_policy_check=lambda envelope: True,
        specialization_feature_enabled=False,
    )

    result = await shell.dispatch(
        TaskEnvelope(
            task_id="task-2",
            intent="summarize",
            payload={"message": "hello"},
            metadata={},
        )
    )

    assert result.route == "core"
    assert result.payload == {"source": "core"}
