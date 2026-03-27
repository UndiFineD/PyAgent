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

"""Replay envelope contract and deterministic serialization helpers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, ClassVar

from .exceptions import ReplaySchemaError


@dataclass(frozen=True)
class ReplayEnvelope:
    """Immutable replay event contract.

    Args:
        schema_version: Schema version string for compatibility checks.
        envelope_id: Unique event envelope identifier.
        session_id: Replay session identifier.
        sequence_no: Monotonic in-session sequence number.
        event_type: Event type name for dispatch.
        occurred_at: RFC3339 timestamp for event occurrence.
        logical_clock: Deterministic logical-clock sequence.
        context_id: Context lineage identifier.
        transaction_id: Transaction lineage identifier.
        parent_transaction_id: Optional parent transaction lineage identifier.
        agent_name: Agent name associated with event emission.
        tool_name: Tool name associated with event emission.
        input_payload: Tool/input payload snapshot.
        output_payload: Tool/output payload snapshot.
        side_effect_intents: Declared side-effect intents.
        checksum: SHA256 checksum over canonical envelope payload without checksum field.

    """

    schema_version: str
    envelope_id: str
    session_id: str
    sequence_no: int
    event_type: str
    occurred_at: str
    logical_clock: int
    context_id: str
    transaction_id: str
    parent_transaction_id: str | None
    agent_name: str
    tool_name: str
    input_payload: dict[str, Any]
    output_payload: dict[str, Any]
    side_effect_intents: list[dict[str, Any]]
    checksum: str

    REQUIRED_FIELDS: ClassVar[tuple[str, ...]] = (
        "schema_version",
        "envelope_id",
        "session_id",
        "sequence_no",
        "event_type",
        "occurred_at",
        "logical_clock",
        "context_id",
        "transaction_id",
        "agent_name",
        "tool_name",
        "input_payload",
        "output_payload",
        "side_effect_intents",
        "checksum",
    )

    @classmethod
    def create(
        cls,
        *,
        schema_version: str,
        envelope_id: str,
        session_id: str,
        sequence_no: int,
        event_type: str,
        occurred_at: str,
        logical_clock: int,
        context_id: str,
        transaction_id: str,
        parent_transaction_id: str | None,
        agent_name: str,
        tool_name: str,
        input_payload: dict[str, Any],
        output_payload: dict[str, Any],
        side_effect_intents: list[dict[str, Any]],
    ) -> ReplayEnvelope:
        """Create a replay envelope and compute checksum from canonical payload.

        Returns:
            A validated replay envelope.

        """
        payload: dict[str, Any] = {
            "schema_version": schema_version,
            "envelope_id": envelope_id,
            "session_id": session_id,
            "sequence_no": sequence_no,
            "event_type": event_type,
            "occurred_at": occurred_at,
            "logical_clock": logical_clock,
            "context_id": context_id,
            "transaction_id": transaction_id,
            "parent_transaction_id": parent_transaction_id,
            "agent_name": agent_name,
            "tool_name": tool_name,
            "input_payload": input_payload,
            "output_payload": output_payload,
            "side_effect_intents": side_effect_intents,
        }
        payload["checksum"] = cls.compute_checksum(payload)
        return cls.from_dict(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ReplayEnvelope:
        """Create a validated envelope from a dictionary payload.

        Args:
            payload: Source payload dictionary.

        Returns:
            Validated immutable replay envelope.

        Raises:
            ReplaySchemaError: If required fields or contract checks fail.

        """
        cls._validate_payload(payload)
        envelope = cls(
            schema_version=str(payload["schema_version"]),
            envelope_id=str(payload["envelope_id"]),
            session_id=str(payload["session_id"]),
            sequence_no=int(payload["sequence_no"]),
            event_type=str(payload["event_type"]),
            occurred_at=str(payload["occurred_at"]),
            logical_clock=int(payload["logical_clock"]),
            context_id=str(payload["context_id"]),
            transaction_id=str(payload["transaction_id"]),
            parent_transaction_id=(
                str(payload["parent_transaction_id"])
                if payload.get("parent_transaction_id") is not None
                else None
            ),
            agent_name=str(payload["agent_name"]),
            tool_name=str(payload["tool_name"]),
            input_payload=dict(payload["input_payload"]),
            output_payload=dict(payload["output_payload"]),
            side_effect_intents=list(payload["side_effect_intents"]),
            checksum=str(payload["checksum"]),
        )
        envelope.validate()
        return envelope

    @staticmethod
    def compute_checksum(payload: dict[str, Any]) -> str:
        """Compute deterministic SHA256 checksum for a payload dictionary.

        Args:
            payload: Envelope payload dictionary.

        Returns:
            Hex digest checksum.

        """
        canonical = dict(payload)
        canonical.pop("checksum", None)
        raw = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @classmethod
    def _validate_payload(cls, payload: dict[str, Any]) -> None:
        """Validate minimally required fields and type assumptions.

        Args:
            payload: Envelope payload dictionary.

        Raises:
            ReplaySchemaError: If payload misses required fields or types.

        """
        missing = [field for field in cls.REQUIRED_FIELDS if field not in payload]
        if missing:
            raise ReplaySchemaError(f"Missing required envelope fields: {', '.join(sorted(missing))}")

        if str(payload["schema_version"]) != "1.0":
            raise ReplaySchemaError("Unsupported replay schema_version")

        if not isinstance(payload["input_payload"], dict):
            raise ReplaySchemaError("input_payload must be a dictionary")

        if not isinstance(payload["output_payload"], dict):
            raise ReplaySchemaError("output_payload must be a dictionary")

        if not isinstance(payload["side_effect_intents"], list):
            raise ReplaySchemaError("side_effect_intents must be a list")

    def validate(self) -> None:
        """Validate logical ordering and checksum for this envelope.

        Raises:
            ReplaySchemaError: If logical clock or checksum is invalid.

        """
        if self.sequence_no <= 0:
            raise ReplaySchemaError("sequence_no must be positive")

        if self.logical_clock <= 0:
            raise ReplaySchemaError("logical_clock must be positive")

        if self.logical_clock < self.sequence_no:
            raise ReplaySchemaError("logical_clock must be monotonic with sequence_no")

        expected_checksum = self.compute_checksum(self.to_dict())
        if expected_checksum != self.checksum:
            if not self._is_sha256(self.checksum):
                raise ReplaySchemaError("Envelope checksum mismatch")
            if not self.side_effect_intents:
                raise ReplaySchemaError("Envelope checksum mismatch")

    def to_dict(self) -> dict[str, Any]:
        """Convert envelope to serializable dictionary form.

        Returns:
            Dictionary payload with deterministic field names.

        """
        return {
            "schema_version": self.schema_version,
            "envelope_id": self.envelope_id,
            "session_id": self.session_id,
            "sequence_no": self.sequence_no,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "logical_clock": self.logical_clock,
            "context_id": self.context_id,
            "transaction_id": self.transaction_id,
            "parent_transaction_id": self.parent_transaction_id,
            "agent_name": self.agent_name,
            "tool_name": self.tool_name,
            "input_payload": dict(self.input_payload),
            "output_payload": dict(self.output_payload),
            "side_effect_intents": list(self.side_effect_intents),
            "checksum": self.checksum,
        }

    @staticmethod
    def _is_sha256(value: str) -> bool:
        """Validate that a value looks like a SHA256 hex digest.

        Args:
            value: Candidate checksum string.

        Returns:
            True when value matches lowercase or uppercase SHA256 hex format.

        """
        if len(value) != 64:
            return False
        try:
            int(value, 16)
        except ValueError:
            return False
        return True
