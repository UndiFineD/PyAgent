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
"""Module-focused red tests for AuditHasher."""

from __future__ import annotations

from importlib import import_module
from typing import Any

import pytest


def _load_symbol(module_name: str, symbol_name: str) -> Any:
    """Load audit symbol with assertion-style red failure behavior."""
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


def test_audithasher_produces_deterministic_hash_for_equivalent_events() -> None:
    """Equivalent events produce the same canonical hash value."""
    audit_event_cls = _load_symbol("AuditEvent", "AuditEvent")
    audit_hasher = _load_symbol("AuditHasher", "AuditHasher")

    event_a = audit_event_cls(
        event_id="evt-1",
        event_type="transaction.commit",
        occurred_at_utc="2026-03-27T12:00:00Z",
        actor_id="agent:test",
        action="commit",
        target="memory",
        tx_id="tx-1",
        context_id="ctx-1",
        correlation_id="corr-1",
        payload={"alpha": 1, "nested": {"a": 1, "b": 2}},
    )
    event_b = audit_event_cls(
        event_id="evt-1",
        event_type="transaction.commit",
        occurred_at_utc="2026-03-27T12:00:00Z",
        actor_id="agent:test",
        action="commit",
        target="memory",
        tx_id="tx-1",
        context_id="ctx-1",
        correlation_id="corr-1",
        payload={"nested": {"b": 2, "a": 1}, "alpha": 1},
    )

    bytes_a = audit_hasher.canonical_event_bytes(event_a)
    bytes_b = audit_hasher.canonical_event_bytes(event_b)
    assert bytes_a == bytes_b
    assert audit_hasher.compute_event_hash("0" * 64, bytes_a) == audit_hasher.compute_event_hash(
        "0" * 64,
        bytes_b,
    )


def test_audithasher_validate_hash_format_accepts_and_rejects_expected_values() -> None:
    """Hash format validation accepts valid SHA-256 hex and rejects invalid forms."""
    audit_hasher = _load_symbol("AuditHasher", "AuditHasher")
    assert audit_hasher.validate_hash_format("a" * 64) is True
    assert audit_hasher.validate_hash_format("A" * 64) is False
    assert audit_hasher.validate_hash_format("f" * 63) is False
    assert audit_hasher.validate_hash_format("xyz") is False
