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

"""Red tests for host validation integration in migrated mixins (AC-MX-002, T004)."""

from __future__ import annotations

import pytest

from src.core.audit.AuditTrailMixin import AuditTrailMixin
from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxMixin import SandboxMixin
from src.core.sandbox.SandboxViolationError import SandboxViolationError


def test_audit_mixin_emits_host_contract_validation_event() -> None:
    """Require audit mixin operations to emit host-contract validation telemetry."""

    class Host(AuditTrailMixin):
        """Host that captures migration events from audit mixin operations."""

        def __init__(self) -> None:
            """Initialize deterministic event capture state."""
            self.events: list[tuple[str, dict[str, object]]] = []

        def _get_audit_trail_core(self) -> None:
            """Return no audit core to focus on contract-validation side effects."""
            return None

        def emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
            """Capture migration events emitted by mixin contract validation hooks."""
            self.events.append((event_name, payload))

    host = Host()
    host.audit_emit_success("save", {"id": "x"})
    assert host.events == [("host_contract_validated", {"mixin": "AuditMixin"})], (
        "Expected audit mixin to emit host_contract_validated event during operation"
    )


def test_sandbox_mixin_emits_contract_error_event_before_rejecting_host() -> None:
    """Require sandbox mixin to emit host-contract error event before violation is raised."""

    class Host(SandboxMixin):
        """Host with deterministic sandbox config and migration event capture."""

        def __init__(self) -> None:
            """Initialize sandbox config and in-memory event ledger."""
            self._sandbox_config = SandboxConfig.from_strings(paths=[], hosts=["allowed.internal"])
            self.events: list[tuple[str, dict[str, object]]] = []

        def emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
            """Capture migration events emitted by mixin validation pathways."""
            self.events.append((event_name, payload))

    host = Host()
    with pytest.raises(SandboxViolationError):
        host._validate_host("blocked.internal")

    assert host.events == [("host_contract_error", {"mixin": "SandboxMixin", "host": "blocked.internal"})], (
        "Expected sandbox mixin to emit host_contract_error event before rejection"
    )
