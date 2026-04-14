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

"""Parity tests for legacy-vs-canonical mixin behavior contracts."""

from __future__ import annotations

import pytest

from tests.core.base.mixins.parity_cases import (
    AuditParityHosts,
    ReplayParityHosts,
    SandboxParityHosts,
    assert_replay_config_failure,
    assert_sandbox_failure,
)


def test_audit_emit_success_behavior_parity(audit_parity_hosts: AuditParityHosts) -> None:
    """Require legacy and canonical audit success behavior parity."""
    legacy_value = audit_parity_hosts.legacy.audit_emit_success("persist", {"ok": True})
    canonical_value = audit_parity_hosts.canonical.audit_emit_success("persist", {"ok": True})
    assert legacy_value == canonical_value == "h" * 64


def test_audit_emit_failure_behavior_parity(audit_parity_hosts: AuditParityHosts) -> None:
    """Require legacy and canonical audit failure behavior parity."""
    legacy_value = audit_parity_hosts.legacy.audit_emit_failure("persist", {"ok": False})
    canonical_value = audit_parity_hosts.canonical.audit_emit_failure("persist", {"ok": False})
    assert legacy_value == canonical_value == "h" * 64


def test_sandbox_host_check_failure_parity(sandbox_parity_hosts: SandboxParityHosts) -> None:
    """Require sandbox failure path equivalence for legacy and canonical hosts."""
    legacy_error = assert_sandbox_failure(sandbox_parity_hosts.legacy)
    canonical_error = assert_sandbox_failure(sandbox_parity_hosts.canonical)
    assert legacy_error == canonical_error == "SandboxViolationError"


@pytest.mark.asyncio
async def test_replay_session_behavior_parity(replay_parity_hosts: ReplayParityHosts) -> None:
    """Require replay-session success parity for legacy and canonical hosts."""
    legacy_payload = await replay_parity_hosts.legacy.replay_session("session-1")
    canonical_payload = await replay_parity_hosts.canonical.replay_session("session-1")
    assert legacy_payload == canonical_payload
    assert legacy_payload["ok"] is True


def test_replay_validation_failure_parity(replay_parity_hosts: ReplayParityHosts) -> None:
    """Require replay configuration failure-path equivalence."""
    legacy_error = assert_replay_config_failure(replay_parity_hosts.legacy)
    canonical_error = assert_replay_config_failure(replay_parity_hosts.canonical)
    assert legacy_error == canonical_error == "ReplayConfigurationError"
