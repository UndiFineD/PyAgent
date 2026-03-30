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

"""Red tests for legacy shim compatibility imports (AC-MX-003, T005-T006)."""

from __future__ import annotations

from importlib import import_module
from typing import Any

import pytest


def test_audit_shim_re_exports_canonical_symbol() -> None:
    """Require legacy audit shim to preserve behavior and declare canonical target path."""
    module = import_module("src.core.audit.AuditTrailMixin")
    shim_target = getattr(module, "__shim_target__", None)

    class FakeCore:
        """Capture append_event_dict usage for parity checks."""

        def append_event_dict(self, **kwargs: Any) -> str:
            """Return deterministic event hash for behavior verification."""
            _ = kwargs
            return "h" * 64

    class Host(module.AuditTrailMixin):
        """Legacy host using shim class under audit module path."""

        def _get_audit_trail_core(self) -> Any:
            """Return fake core for deterministic behavior validation."""
            return FakeCore()

    result = Host().audit_emit_success("persist", {"ok": True})
    assert result == "h" * 64
    assert shim_target == "src.core.base.mixins.audit_mixin.AuditMixin", (
        f"Expected canonical shim target metadata, got {shim_target!r}"
    )


def test_sandbox_shim_re_exports_canonical_symbol() -> None:
    """Require legacy sandbox shim to preserve behavior and declare canonical target path."""
    module = import_module("src.core.sandbox.SandboxMixin")
    shim_target = getattr(module, "__shim_target__", None)

    class Host(module.SandboxMixin):
        """Legacy host using shim class under sandbox module path."""

        def __init__(self) -> None:
            """Initialize restrictive sandbox policy for failure-path behavior checks."""
            self._sandbox_config = module.SandboxConfig.from_strings(paths=[], hosts=["good.internal"])

    with pytest.raises(module.SandboxViolationError):
        Host()._validate_host("bad.internal")

    assert shim_target == "src.core.base.mixins.sandbox_mixin.SandboxMixin", (
        f"Expected canonical shim target metadata, got {shim_target!r}"
    )


@pytest.mark.asyncio
async def test_replay_shim_re_exports_canonical_symbol() -> None:
    """Require legacy replay shim to preserve behavior and declare canonical target path."""
    module = import_module("src.core.replay.ReplayMixin")
    shim_target = getattr(module, "__shim_target__", None)

    class FakeOrchestrator:
        """Deterministic replay orchestrator for shim behavior checks."""

        async def replay_session(
            self,
            session_id: str,
            *,
            mode: str = "replay",
            stop_on_divergence: bool = True,
        ) -> dict[str, object]:
            """Return replay payload for parity validation."""
            _ = (session_id, mode, stop_on_divergence)
            return {"ok": True}

    class Host(module.ReplayMixin):
        """Legacy host using shim class under replay module path."""

        def __init__(self) -> None:
            """Initialize replay dependencies for deterministic parity check."""
            self._replay_orchestrator = FakeOrchestrator()

    payload = await Host().replay_session("s1")
    assert payload == {"ok": True}
    assert shim_target == "src.core.base.mixins.replay_mixin.ReplayMixin", (
        f"Expected canonical shim target metadata, got {shim_target!r}"
    )
