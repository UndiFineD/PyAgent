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

"""Per-module red tests for ReplayOrchestrator contract module."""

from __future__ import annotations

from typing import Any

import pytest

from tests.test_shadow_replay import _build_envelope, _require_symbol


@pytest.mark.asyncio
async def test_replay_orchestrator_replay_session_returns_summary() -> None:
    """Verify replay_session returns a structured summary object."""
    replay_orchestrator_cls = _require_symbol("ReplayOrchestrator", "ReplayOrchestrator")

    class _Store:
        """Provide a contiguous replay stream."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return deterministic envelope stream."""
            return [
                _build_envelope(sequence_no=1, session_id="s-module-orchestrator"),
                _build_envelope(sequence_no=2, session_id="s-module-orchestrator"),
            ]

    class _ShadowCore:
        """Return deterministic success for each envelope."""

        async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int | None = None) -> Any:
            """Return generic success object."""
            return type("ReplayStepResult", (), {"success": True})()

    summary = await replay_orchestrator_cls(store=_Store(), shadow_core=_ShadowCore()).replay_session(
        "s-module-orchestrator",
        mode="replay",
    )

    assert summary is not None
