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

"""Observability event contract tests for mixin migration flows."""

from __future__ import annotations

from src.core.base.mixins.migration_observability import MigrationObservability, emit_migration_event


def test_collector_counts_all_required_migration_events() -> None:
    """Require collector to record usage and failure event families."""
    collector = MigrationObservability()
    for event_name in ("shim_used", "parity_failed", "import_error", "host_contract_error"):
        collector.emit(event_name, {"source": "test"})

    snapshot = collector.snapshot_counts()
    assert snapshot["shim_used"] == 1
    assert snapshot["parity_failed"] == 1
    assert snapshot["import_error"] == 1
    assert snapshot["host_contract_error"] == 1


def test_emit_migration_event_calls_host_and_collector() -> None:
    """Require helper to dispatch to host callback and optional collector."""

    class Host:
        """Capture host callback invocations for migration event tests."""

        def __init__(self) -> None:
            """Initialize callback capture list."""
            self.calls: list[tuple[str, dict[str, object]]] = []

        def emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
            """Record migration event callback arguments."""
            self.calls.append((event_name, payload))

    host = Host()
    collector = MigrationObservability()
    emitted = emit_migration_event(
        host=host,
        event_name="shim_used",
        payload={"module": "src.core.audit.AuditTrailMixin"},
        collector=collector,
    )

    assert host.calls == [("shim_used", {"module": "src.core.audit.AuditTrailMixin"})]
    assert emitted is not None
    assert emitted.event_name == "shim_used"
    assert collector.count("shim_used") == 1


def test_emit_migration_event_without_host_callback_still_collects() -> None:
    """Require helper to collect events even when host has no callback."""

    class Host:
        """Host without an emit callback to exercise fallback path."""

    collector = MigrationObservability()
    emitted = emit_migration_event(
        host=Host(),
        event_name="import_error",
        payload={"module": "src.core.base.mixins.replay_mixin", "error": "ImportError"},
        collector=collector,
    )

    assert emitted is not None
    assert emitted.payload["error"] == "ImportError"
    assert collector.count("import_error") == 1
