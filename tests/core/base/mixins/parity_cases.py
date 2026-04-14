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

"""Shared parity fixtures and host fakes for legacy-vs-canonical tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.audit.AuditTrailMixin import AuditTrailMixin as LegacyAuditMixin
from src.core.base.mixins.audit_mixin import AuditMixin as CanonicalAuditMixin
from src.core.base.mixins.replay_mixin import ReplayMixin as CanonicalReplayMixin
from src.core.base.mixins.sandbox_mixin import SandboxMixin as CanonicalSandboxMixin
from src.core.replay.exceptions import ReplayConfigurationError
from src.core.replay.ReplayMixin import ReplayMixin as LegacyReplayMixin
from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxMixin import SandboxMixin as LegacySandboxMixin
from src.core.sandbox.SandboxViolationError import SandboxViolationError


class _FakeAuditCore:
    """Provide deterministic audit-core behavior for parity assertions."""

    def append_event_dict(self, **kwargs: Any) -> str:
        """Return deterministic event hash for parity tests.

        Args:
            **kwargs: Event payload fields.

        Returns:
            Deterministic event-hash string.

        """
        _ = kwargs
        return "h" * 64


class _FakeReplayOrchestrator:
    """Provide deterministic replay orchestration responses."""

    async def replay_session(
        self,
        session_id: str,
        *,
        mode: str = "replay",
        stop_on_divergence: bool = True,
    ) -> dict[str, object]:
        """Return deterministic replay payload.

        Args:
            session_id: Replay session identifier.
            mode: Replay mode.
            stop_on_divergence: Divergence stop flag.

        Returns:
            Replay payload dictionary.

        """
        return {
            "session_id": session_id,
            "mode": mode,
            "stop_on_divergence": stop_on_divergence,
            "ok": True,
        }


@dataclass
class AuditParityHosts:
    """Container for legacy and canonical audit test hosts."""

    legacy: LegacyAuditMixin
    canonical: CanonicalAuditMixin


@dataclass
class SandboxParityHosts:
    """Container for legacy and canonical sandbox test hosts."""

    legacy: LegacySandboxMixin
    canonical: CanonicalSandboxMixin


@dataclass
class ReplayParityHosts:
    """Container for legacy and canonical replay test hosts."""

    legacy: LegacyReplayMixin
    canonical: CanonicalReplayMixin


def make_audit_parity_hosts() -> AuditParityHosts:
    """Create legacy and canonical audit hosts with identical behavior.

    Returns:
        Hosts configured for audit parity checks.

    """

    class LegacyAuditHost(LegacyAuditMixin):
        """Legacy-path host using audit shim class."""

        def _get_audit_trail_core(self) -> Any:
            """Return deterministic test audit core."""
            return _FakeAuditCore()

    class CanonicalAuditHost(CanonicalAuditMixin):
        """Canonical-path host using canonical audit mixin class."""

        def _get_audit_trail_core(self) -> Any:
            """Return deterministic test audit core."""
            return _FakeAuditCore()

    return AuditParityHosts(legacy=LegacyAuditHost(), canonical=CanonicalAuditHost())


def make_sandbox_parity_hosts() -> SandboxParityHosts:
    """Create legacy and canonical sandbox hosts with identical config.

    Returns:
        Hosts configured for sandbox parity checks.

    """

    class LegacySandboxHost(LegacySandboxMixin):
        """Legacy-path sandbox host."""

        def __init__(self) -> None:
            """Seed deterministic sandbox allow-list for parity tests."""
            self._sandbox_config = SandboxConfig.from_strings(paths=[], hosts=["good.internal"])

    class CanonicalSandboxHost(CanonicalSandboxMixin):
        """Canonical-path sandbox host."""

        def __init__(self) -> None:
            """Seed deterministic sandbox allow-list for parity tests."""
            self._sandbox_config = SandboxConfig.from_strings(paths=[], hosts=["good.internal"])

    return SandboxParityHosts(legacy=LegacySandboxHost(), canonical=CanonicalSandboxHost())


def make_replay_parity_hosts() -> ReplayParityHosts:
    """Create legacy and canonical replay hosts with same orchestrator.

    Returns:
        Hosts configured for replay parity checks.

    """

    class LegacyReplayHost(LegacyReplayMixin):
        """Legacy-path replay host."""

        def __init__(self) -> None:
            """Seed deterministic replay orchestrator dependency."""
            self._replay_orchestrator = _FakeReplayOrchestrator()

    class CanonicalReplayHost(CanonicalReplayMixin):
        """Canonical-path replay host."""

        def __init__(self) -> None:
            """Seed deterministic replay orchestrator dependency."""
            self._replay_orchestrator = _FakeReplayOrchestrator()

    return ReplayParityHosts(legacy=LegacyReplayHost(), canonical=CanonicalReplayHost())


def assert_sandbox_failure(host: CanonicalSandboxMixin) -> str:
    """Run deterministic sandbox failure path and return exception type.

    Args:
        host: Configured sandbox host.

    Returns:
        Exception class name raised by host validation.

    Raises:
        AssertionError: Sandbox failure path does not raise expected exception.

    """
    try:
        host._validate_host("blocked.internal")
    except SandboxViolationError as exc:
        return exc.__class__.__name__

    raise AssertionError("Expected sandbox host validation failure")


def assert_replay_config_failure(host: CanonicalReplayMixin) -> str:
    """Run deterministic replay configuration failure path.

    Args:
        host: Replay host with intentionally invalid dependency.

    Returns:
        Replay exception class name.

    Raises:
        AssertionError: Replay validation did not fail as expected.

    """
    host._replay_orchestrator = object()
    try:
        host.validate()
    except ReplayConfigurationError as exc:
        return exc.__class__.__name__

    raise AssertionError("Expected replay validation failure")


__all__ = [
    "AuditParityHosts",
    "SandboxParityHosts",
    "ReplayParityHosts",
    "make_audit_parity_hosts",
    "make_sandbox_parity_hosts",
    "make_replay_parity_hosts",
    "assert_sandbox_failure",
    "assert_replay_config_failure",
]
