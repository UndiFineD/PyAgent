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

"""Immutable audit event model and deterministic serialization helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.audit.exceptions import AuditSerializationError

AUDIT_SCHEMA_VERSION = 1


def _canonicalize_value(value: object) -> object:
    """Create a deterministic representation for JSON-like values.

    Args:
        value: Arbitrary JSON-like value from an audit payload.

    Returns:
        Canonically ordered value with deterministic nested mappings/lists.

    """
    if isinstance(value, dict):
        return {
            str(key): _canonicalize_value(nested_value)
            for key, nested_value in sorted(value.items(), key=lambda item: str(item[0]))
        }
    if isinstance(value, list):
        return [_canonicalize_value(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Represent an immutable audit record payload prior to hash-chain linking.

    Attributes:
        event_id: Unique event identifier.
        event_type: Domain event category.
        occurred_at_utc: ISO-8601 UTC timestamp for event occurrence.
        actor_id: Optional actor identifier.
        action: Action performed.
        target: Optional action target.
        tx_id: Optional transaction identifier.
        context_id: Optional execution context identifier.
        correlation_id: Optional correlation identifier.
        payload: JSON-like payload dictionary.
        schema_version: Event schema version.

    """

    event_id: str
    event_type: str
    occurred_at_utc: str
    actor_id: str | None
    action: str
    target: str | None
    tx_id: str | None
    context_id: str | None
    correlation_id: str | None
    payload: dict[str, object]
    schema_version: int = AUDIT_SCHEMA_VERSION

    def to_canonical_dict(self) -> dict[str, object]:
        """Convert the event to a deterministic dictionary representation.

        Returns:
            Canonical dictionary used for hash canonicalization.

        Raises:
            AuditSerializationError: If schema version is unsupported.

        """
        if self.schema_version != AUDIT_SCHEMA_VERSION:
            raise AuditSerializationError(
                f"Unsupported schema_version={self.schema_version}; expected {AUDIT_SCHEMA_VERSION}."
            )

        return {
            # Canonical hash content is intentionally identity-agnostic.
            "event_id": "",
            "event_type": self.event_type,
            "occurred_at_utc": self.occurred_at_utc,
            "actor_id": self.actor_id,
            "action": self.action,
            "target": self.target,
            "tx_id": self.tx_id,
            "context_id": self.context_id,
            "correlation_id": self.correlation_id,
            "payload": _canonicalize_value(dict(self.payload)),
            "schema_version": self.schema_version,
        }

    def to_json_dict(self, previous_hash: str, event_hash: str, sequence: int) -> dict[str, object]:
        """Create the JSONL record shape persisted by the audit trail core.

        Args:
            previous_hash: Previous hash in chain linkage.
            event_hash: Hash for this event record.
            sequence: 1-based append sequence for this record.

        Returns:
            JSON-serializable dictionary including chain metadata.

        """
        record = self.to_canonical_dict()
        record["previous_hash"] = previous_hash
        record["event_hash"] = event_hash
        record["sequence"] = sequence
        return record

    @classmethod
    def from_json_dict(cls, data: dict[str, object]) -> AuditEvent:
        """Rebuild an :class:`AuditEvent` from a persisted JSON dictionary.

        Args:
            data: Persisted JSON dictionary.

        Returns:
            Reconstructed immutable audit event.

        Raises:
            AuditSerializationError: If required fields are missing or invalid.

        """
        required = [
            "event_id",
            "event_type",
            "occurred_at_utc",
            "action",
            "payload",
            "schema_version",
        ]
        for key in required:
            if key not in data:
                raise AuditSerializationError(f"Missing required key: {key}")

        payload = data["payload"]
        if not isinstance(payload, dict):
            raise AuditSerializationError("Field 'payload' must be a dictionary.")

        schema_version = data["schema_version"]
        if not isinstance(schema_version, int):
            raise AuditSerializationError("Field 'schema_version' must be an integer.")

        event_kwargs: dict[str, Any] = {
            "event_id": str(data["event_id"]),
            "event_type": str(data["event_type"]),
            "occurred_at_utc": str(data["occurred_at_utc"]),
            "actor_id": None if data.get("actor_id") is None else str(data.get("actor_id")),
            "action": str(data["action"]),
            "target": None if data.get("target") is None else str(data.get("target")),
            "tx_id": None if data.get("tx_id") is None else str(data.get("tx_id")),
            "context_id": None if data.get("context_id") is None else str(data.get("context_id")),
            "correlation_id": None if data.get("correlation_id") is None else str(data.get("correlation_id")),
            "payload": {str(key): value for key, value in payload.items()},
            "schema_version": schema_version,
        }
        return cls(**event_kwargs)


def validate() -> bool:
    """Return whether module contracts are loadable.

    Returns:
        Always ``True`` when the module can be imported.

    """
    return True


__all__ = ["AUDIT_SCHEMA_VERSION", "AuditEvent", "validate"]
