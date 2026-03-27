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

"""Agent-facing replay mixin APIs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .exceptions import ReplayConfigurationError
from .ReplayEnvelope import ReplayEnvelope


class ReplayMixin:
    """Expose replay emission and replay-session delegation helpers."""

    def validate(self) -> None:
        """Validate replay mixin host dependencies.

        Raises:
            ReplayConfigurationError: If replay orchestrator dependency is invalid.

        """
        orchestrator = getattr(self, "_replay_orchestrator", None)
        if orchestrator is not None and not hasattr(orchestrator, "replay_session"):
            raise ReplayConfigurationError("Replay orchestrator must expose replay_session")

    async def emit_replay_envelope(
        self,
        *,
        event_type: str,
        input_payload: dict[str, Any],
        output_payload: dict[str, Any],
        side_effect_intents: list[dict[str, Any]],
        session_id: str | None = None,
        tool_name: str = "unknown_tool",
    ) -> ReplayEnvelope:
        """Emit one replay envelope with lineage fields populated from host state.

        Args:
            event_type: Replay event type name.
            input_payload: Input payload snapshot.
            output_payload: Output payload snapshot.
            side_effect_intents: Declared side-effect intents.
            session_id: Optional explicit session id.
            tool_name: Tool name for event metadata.

        Returns:
            Constructed and validated replay envelope.

        """
        self.validate()

        sequence_no = int(getattr(self, "_replay_sequence_no", 0)) + 1
        self._replay_sequence_no = sequence_no

        resolved_session_id = session_id or str(getattr(self, "_replay_session_id", "default-session"))
        occurred_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        parent_transaction_id = getattr(self, "parent_transaction_id", None)

        envelope = ReplayEnvelope.create(
            schema_version="1.0",
            envelope_id=f"env-{resolved_session_id}-{sequence_no}",
            session_id=resolved_session_id,
            sequence_no=sequence_no,
            event_type=event_type,
            occurred_at=occurred_at,
            logical_clock=sequence_no,
            context_id=str(getattr(self, "context_id", f"ctx-{uuid4()}")),
            transaction_id=str(getattr(self, "transaction_id", f"tx-{uuid4()}")),
            parent_transaction_id=(str(parent_transaction_id) if parent_transaction_id is not None else None),
            agent_name=str(getattr(self, "name", self.__class__.__name__)),
            tool_name=tool_name,
            input_payload=input_payload,
            output_payload=output_payload,
            side_effect_intents=side_effect_intents,
        )

        replay_store = getattr(self, "_replay_store", None)
        if replay_store is not None and hasattr(replay_store, "append_envelope"):
            await replay_store.append_envelope(envelope)

        return envelope

    async def replay_session(
        self,
        session_id: str,
        *,
        mode: str = "replay",
        stop_on_divergence: bool = True,
    ) -> Any:
        """Delegate replay execution to orchestrator dependency.

        Args:
            session_id: Session identifier.
            mode: Replay mode descriptor.
            stop_on_divergence: Whether to stop on first divergence.

        Returns:
            Replay result from orchestrator.

        Raises:
            ReplayConfigurationError: If orchestrator dependency is missing.

        """
        self.validate()
        orchestrator = getattr(self, "_replay_orchestrator", None)
        if orchestrator is None:
            raise ReplayConfigurationError("Replay orchestrator is not configured")

        return await orchestrator.replay_session(
            session_id,
            mode=mode,
            stop_on_divergence=stop_on_divergence,
        )
