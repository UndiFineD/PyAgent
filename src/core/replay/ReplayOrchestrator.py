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

"""Replay orchestration control flow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .exceptions import ReplayConfigurationError, ReplaySequenceError
from .ReplayEnvelope import ReplayEnvelope


@dataclass
class ReplayDivergence:
    """Represents one replay divergence event.

    Args:
        sequence_no: Sequence number where divergence occurred.
        reason: Diagnostic reason for divergence.

    """

    sequence_no: int
    reason: str


@dataclass
class ReplaySessionSummary:
    """Summary for one replay session execution.

    Args:
        session_id: Session identifier.
        mode: Replay mode used.
        total_steps: Total envelopes loaded.
        executed_steps: Steps actually executed.
        success: True when no divergences were detected.
        divergences: Collected divergence records.

    """

    session_id: str
    mode: str
    total_steps: int
    executed_steps: int
    success: bool
    divergences: list[ReplayDivergence] = field(default_factory=list)


class ReplayOrchestrator:
    """Coordinate deterministic replay execution across envelope streams."""

    def __init__(self, *, store: Any, shadow_core: Any) -> None:
        """Initialize replay orchestrator dependencies.

        Args:
            store: Replay store dependency.
            shadow_core: Shadow execution core dependency.

        """
        self._store = store
        self._shadow_core = shadow_core

    def validate(self) -> None:
        """Validate orchestrator dependencies.

        Raises:
            ReplayConfigurationError: If dependency contracts are missing.

        """
        if not hasattr(self._store, "load_session"):
            raise ReplayConfigurationError("Replay store must expose load_session")

        if not hasattr(self._shadow_core, "execute_envelope"):
            raise ReplayConfigurationError("Shadow core must expose execute_envelope")

    async def replay_session(
        self,
        session_id: str,
        *,
        mode: str = "replay",
        stop_on_divergence: bool = True,
    ) -> ReplaySessionSummary:
        """Replay a full session in deterministic order.

        Args:
            session_id: Session identifier.
            mode: Execution mode descriptor.
            stop_on_divergence: Whether to stop on first divergence.

        Returns:
            Structured replay session summary.

        Raises:
            ReplaySequenceError: If loaded envelopes are not contiguous.

        """
        self.validate()

        envelopes: list[ReplayEnvelope] = await self._store.load_session(session_id)
        self._validate_contiguous_sequence(envelopes)

        divergences: list[ReplayDivergence] = []
        executed_steps = 0

        for envelope in envelopes:
            executed_steps += 1
            step_result = await self._shadow_core.execute_envelope(
                envelope,
                deterministic_seed=envelope.logical_clock,
            )

            if not bool(getattr(step_result, "success", False)):
                reason = str(getattr(step_result, "reason", "diverged"))
                divergences.append(ReplayDivergence(sequence_no=envelope.sequence_no, reason=reason))
                if stop_on_divergence:
                    break

        return ReplaySessionSummary(
            session_id=session_id,
            mode=mode,
            total_steps=len(envelopes),
            executed_steps=executed_steps,
            success=len(divergences) == 0,
            divergences=divergences,
        )

    def _validate_contiguous_sequence(self, envelopes: list[ReplayEnvelope]) -> None:
        """Validate that sequence numbers are contiguous for replay.

        Args:
            envelopes: Loaded envelope list.

        Raises:
            ReplaySequenceError: If a sequence gap is detected.

        """
        if not envelopes:
            return

        expected = envelopes[0].sequence_no
        for envelope in envelopes:
            if envelope.sequence_no != expected:
                raise ReplaySequenceError(
                    f"Sequence gap in replay session: expected {expected}, got {envelope.sequence_no}"
                )
            expected += 1
