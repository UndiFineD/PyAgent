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
"""Module-focused red tests for AuditEvent."""
from __future__ import annotations

from importlib import import_module
from typing import Any

import pytest


def _load_auditevent() -> Any:
    """Load AuditEvent with assertion-style red failure on missing module/symbol."""
    try:
        module = import_module("src.core.audit.AuditEvent")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing src.core.audit.AuditEvent implementation: {exc}", pytrace=False)
    if not hasattr(module, "AuditEvent"):
        pytest.fail("Missing AuditEvent class in src.core.audit.AuditEvent", pytrace=False)
    return module.AuditEvent


def test_auditevent_exposes_canonical_methods() -> None:
    """AuditEvent exposes canonical serialization API methods."""
    audit_event_cls = _load_auditevent()
    assert hasattr(audit_event_cls, "to_canonical_dict")
    assert hasattr(audit_event_cls, "to_json_dict")
    assert hasattr(audit_event_cls, "from_json_dict")


def test_auditevent_schema_version_default_is_one() -> None:
    """AuditEvent defaults schema_version to 1 when omitted."""
    audit_event_cls = _load_auditevent()
    event = audit_event_cls(
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
    assert event.schema_version == 1
