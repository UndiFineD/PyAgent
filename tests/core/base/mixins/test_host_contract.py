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

"""Red tests for host contract and base behavior mixin (AC-MX-002, T003)."""

from __future__ import annotations

import pytest

from src.core.audit.AuditTrailMixin import AuditTrailMixin


def test_validate_host_contract_rejects_missing_host_methods() -> None:
    """Require host-contract validation to reject a host missing required capabilities."""

    class HostMissingContext(AuditTrailMixin):
        """Host that intentionally omits required host contract methods."""

        logger = object()

    host = HostMissingContext()
    with pytest.raises(ValueError, match="get_runtime_context"):
        host.validate_host_contract()


def test_validate_host_contract_accepts_complete_host() -> None:
    """Require host-contract validation to pass for a host with required capabilities."""

    class HostWithContract(AuditTrailMixin):
        """Host implementing expected contract methods for canonical validation."""

        logger = object()

        def get_runtime_context(self) -> dict[str, object]:
            """Return minimal context payload for host contract tests."""
            return {"ok": True}

        def emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
            """Accept migration events for host contract checks."""
            _ = (event_name, payload)

    host = HostWithContract()
    host.validate_host_contract()
    assert host.get_runtime_context() == {"ok": True}
