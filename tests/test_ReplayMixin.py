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

"""Per-module red tests for ReplayMixin contract module."""

from __future__ import annotations

from typing import Any

import pytest

from tests.test_shadow_replay import _require_symbol


@pytest.mark.asyncio
async def test_replay_mixin_replay_session_delegates_with_flag() -> None:
    """Verify ReplayMixin replay API delegates to orchestrator call."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")

    class _Orchestrator:
        """Record replay calls and return deterministic payload."""

        def __init__(self) -> None:
            """Initialize captured call store."""
            self.captured: list[tuple[str, bool]] = []

        async def replay_session(
            self,
            session_id: str,
            *,
            mode: str = "replay",
            stop_on_divergence: bool = True,
        ) -> dict[str, Any]:
            """Capture replay delegation and return deterministic output."""
            self.captured.append((session_id, stop_on_divergence))
            return {"ok": True}

    class _Host(replay_mixin_cls):
        """Minimal mixin host with orchestrator dependency."""

        def __init__(self) -> None:
            """Initialize replay dependencies for delegation test."""
            self._replay_store = None
            self._replay_orchestrator = _Orchestrator()

    host = _Host()
    result = await host.replay_session("s-module-mixin", stop_on_divergence=False)

    assert result["ok"] is True
    assert host._replay_orchestrator.captured == [("s-module-mixin", False)]
