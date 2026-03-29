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
"""Module-focused red tests for AuditTrailMixin."""

from __future__ import annotations

from importlib import import_module
from typing import Any

import pytest


def _load_mixin() -> Any:
    """Load AuditTrailMixin with assertion-style red failure behavior."""
    try:
        module = import_module("src.core.audit.AuditTrailMixin")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing src.core.audit.AuditTrailMixin implementation: {exc}", pytrace=False)
    if not hasattr(module, "AuditTrailMixin"):
        pytest.fail("Missing AuditTrailMixin class in src.core.audit.AuditTrailMixin", pytrace=False)
    return module.AuditTrailMixin


def test_audittrailmixin_returns_none_when_no_core() -> None:
    """audit_emit_event returns None when host returns no core."""
    audit_trail_mixin_cls = _load_mixin()

    class _Host(audit_trail_mixin_cls):
        """Host that does not provide an audit core."""

        def _get_audit_trail_core(self) -> Any:
            """Return no core for null-path behavior."""
            return None

    host = _Host()
    result = host.audit_emit_event(
        event_type="transaction.commit",
        action="commit",
        payload={"ok": True},
    )
    assert result is None


def test_audittrailmixin_delegates_to_core_append_event_dict() -> None:
    """audit_emit_event delegates to append_event_dict on configured core."""
    audit_trail_mixin_cls = _load_mixin()

    class _FakeCore:
        """Minimal fake core capturing append_event_dict calls."""

        def __init__(self) -> None:
            """Initialize call capture and deterministic return value."""
            self.calls: list[dict[str, Any]] = []

        def append_event_dict(self, **kwargs: Any) -> str:
            """Capture kwargs and return deterministic hash token."""
            self.calls.append(kwargs)
            return "a" * 64

    class _Host(audit_trail_mixin_cls):
        """Host returning a fake core for delegation checks."""

        def __init__(self) -> None:
            """Create host with fake core instance."""
            self.core = _FakeCore()

        def _get_audit_trail_core(self) -> Any:
            """Return fake core instance."""
            return self.core

    host = _Host()
    result = host.audit_emit_event(
        event_type="transaction.commit",
        action="commit",
        payload={"step": 1},
    )
    assert result == "a" * 64
    assert len(host.core.calls) == 1
