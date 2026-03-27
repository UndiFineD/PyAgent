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
"""Module-focused red tests for AuditTrailCore."""
from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any

import pytest


def _load_symbol(module_name: str, symbol_name: str) -> Any:
    """Load audit symbol with assertion-based red failure behavior."""
    try:
        module = import_module(f"src.core.audit.{module_name}")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing src.core.audit.{module_name} implementation: {exc}", pytrace=False)
    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Missing symbol {symbol_name} in src.core.audit.{module_name}",
            pytrace=False,
        )
    return getattr(module, symbol_name)


def _new_event() -> Any:
    """Create a contract-compliant AuditEvent for core API tests."""
    audit_event_cls = _load_symbol("AuditEvent", "AuditEvent")
    return audit_event_cls(
        event_id="evt-1",
        event_type="transaction.commit",
        occurred_at_utc="2026-03-27T12:00:00Z",
        actor_id="agent:test",
        action="commit",
        target="memory",
        tx_id="tx-1",
        context_id="ctx-1",
        correlation_id="corr-1",
        payload={"k": "v"},
    )


def test_audittrailcore_append_event_returns_hash_string(tmp_path: Path) -> None:
    """append_event returns a lowercase SHA-256 hash string."""
    audit_trail_core_cls = _load_symbol("AuditTrailCore", "AuditTrailCore")
    core = audit_trail_core_cls(str(tmp_path / "audit.jsonl"), fail_closed=True)
    event_hash = core.append_event(_new_event())
    assert isinstance(event_hash, str)
    assert len(event_hash) == 64


def test_audittrailcore_verify_file_returns_result_object(tmp_path: Path) -> None:
    """verify_file returns an AuditVerificationResult-like object with validity fields."""
    audit_trail_core_cls = _load_symbol("AuditTrailCore", "AuditTrailCore")
    core = audit_trail_core_cls(str(tmp_path / "audit.jsonl"), fail_closed=True)
    core.append_event(_new_event())
    result = core.verify_file()
    assert hasattr(result, "is_valid")
    assert hasattr(result, "total_events")
    assert hasattr(result, "validated_events")
