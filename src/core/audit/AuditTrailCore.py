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

"""Append-only immutable audit hash-chain orchestration core."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.core.audit.AuditEvent import AUDIT_SCHEMA_VERSION, AuditEvent
from src.core.audit.AuditHasher import AuditHasher
from src.core.audit.AuditVerificationResult import AuditVerificationResult
from src.core.audit.exceptions import (
    AuditChainLinkError,
    AuditIntegrityError,
    AuditPersistenceError,
    AuditSerializationError,
)

GENESIS_PREVIOUS_HASH = "0" * 64


class AuditTrailCore:
    """Manage immutable append and verification operations for audit records."""

    def __init__(self, audit_file_path: str, *, fail_closed: bool = True) -> None:
        """Initialize the audit trail core.

        Args:
            audit_file_path: Path to JSONL audit file.
            fail_closed: Raise exceptions for persistence/serialization failures.

        """
        self.audit_file_path = audit_file_path
        self._audit_file_path = audit_file_path
        self._path = Path(audit_file_path)
        self._fail_closed = fail_closed

    def append_event(self, event: AuditEvent) -> str:
        """Append an audit event to the JSONL chain.

        Args:
            event: Immutable event to append.

        Returns:
            Computed event hash for the appended record.

        Raises:
            AuditPersistenceError: If writing fails under fail-closed mode.
            AuditSerializationError: If event serialization fails under fail-closed mode.

        """
        try:
            previous_hash = self.get_last_hash()
            sequence = self.get_last_sequence() + 1
            event_bytes = AuditHasher.canonical_event_bytes(event)
            event_hash = AuditHasher.compute_event_hash(previous_hash, event_bytes)
            record = event.to_json_dict(previous_hash=previous_hash, event_hash=event_hash, sequence=sequence)
            self._append_record(record)
            return event_hash
        except (AuditSerializationError, AuditPersistenceError):
            if self._fail_closed:
                raise
            return ""
        except OSError as exc:
            if self._fail_closed:
                raise AuditPersistenceError(str(exc)) from exc
            return ""

    def append_event_dict(
        self,
        *,
        event_type: str,
        action: str,
        payload: dict[str, object],
        actor_id: str | None = None,
        target: str | None = None,
        tx_id: str | None = None,
        context_id: str | None = None,
        correlation_id: str | None = None,
        occurred_at_utc: str | None = None,
        event_id: str | None = None,
    ) -> str:
        """Construct and append an audit event from primitive values.

        Args:
            event_type: Domain event category.
            action: Action performed.
            payload: JSON-like payload object.
            actor_id: Optional actor identifier.
            target: Optional target identifier.
            tx_id: Optional transaction identifier.
            context_id: Optional context identifier.
            correlation_id: Optional correlation identifier.
            occurred_at_utc: Optional explicit timestamp; defaults to current UTC.
            event_id: Optional explicit event id; defaults to generated UUID.

        Returns:
            Computed event hash for the appended record.

        """
        resolved_occurred_at_utc = occurred_at_utc or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        resolved_event_id = event_id or str(uuid4())

        event = AuditEvent(
            event_id=resolved_event_id,
            event_type=event_type,
            occurred_at_utc=resolved_occurred_at_utc,
            actor_id=actor_id,
            action=action,
            target=target,
            tx_id=tx_id,
            context_id=context_id,
            correlation_id=correlation_id,
            payload=dict(payload),
            schema_version=AUDIT_SCHEMA_VERSION,
        )
        return self.append_event(event)

    def iter_records(self) -> list[dict[str, object]]:
        """Return all persisted records in append order.

        Returns:
            List of decoded record dictionaries in file order.

        Raises:
            AuditPersistenceError: If file reading fails.
            AuditSerializationError: If a line cannot be decoded.

        """
        if not self._path.exists():
            return []

        records: list[dict[str, object]] = []
        try:
            with self._path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    decoded = json.loads(stripped)
                    if not isinstance(decoded, dict):
                        raise AuditSerializationError("Audit record must decode to a JSON object.")
                    records.append({str(key): value for key, value in decoded.items()})
        except json.JSONDecodeError as exc:
            raise AuditSerializationError(str(exc)) from exc
        except OSError as exc:
            raise AuditPersistenceError(str(exc)) from exc
        return records

    def verify_file(self) -> AuditVerificationResult:
        """Replay and validate the full audit hash-chain.

        Returns:
            Structured verification result including first failure metadata.

        """
        if not self._path.exists():
            return AuditVerificationResult(
                is_valid=True,
                total_events=0,
                validated_events=0,
                first_invalid_sequence=None,
                error_code=None,
                error_message=None,
                last_valid_hash=None,
            )

        expected_previous_hash = GENESIS_PREVIOUS_HASH
        total_events = 0
        validated_events = 0
        last_valid_hash: str | None = None

        try:
            with self._path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    stripped = line.strip()
                    if not stripped:
                        continue

                    total_events += 1
                    try:
                        decoded = json.loads(stripped)
                    except json.JSONDecodeError as exc:
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="MALFORMED_JSON",
                            error_message=str(exc),
                            last_valid_hash=last_valid_hash,
                        )

                    if not isinstance(decoded, dict):
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="MALFORMED_RECORD",
                            error_message="Record is not a JSON object.",
                            last_valid_hash=last_valid_hash,
                        )

                    record: dict[str, object] = {str(key): value for key, value in decoded.items()}
                    previous_hash = record.get("previous_hash")
                    event_hash = record.get("event_hash")
                    if not isinstance(previous_hash, str) or not isinstance(event_hash, str):
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="HASH_FORMAT",
                            error_message="Record hash fields are missing or invalid.",
                            last_valid_hash=last_valid_hash,
                        )

                    if not AuditHasher.validate_hash_format(previous_hash) or not AuditHasher.validate_hash_format(
                        event_hash
                    ):
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="HASH_FORMAT",
                            error_message="Record hash fields are not lowercase SHA-256 hex.",
                            last_valid_hash=last_valid_hash,
                        )

                    if previous_hash != expected_previous_hash:
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="CHAIN_LINK",
                            error_message="previous_hash does not match the prior event hash.",
                            last_valid_hash=last_valid_hash,
                        )

                    try:
                        event = AuditEvent.from_json_dict(record)
                    except AuditSerializationError as exc:
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="SERIALIZATION",
                            error_message=str(exc),
                            last_valid_hash=last_valid_hash,
                        )

                    canonical_bytes = AuditHasher.canonical_event_bytes(event)
                    expected_event_hash = AuditHasher.compute_event_hash(previous_hash, canonical_bytes)
                    if expected_event_hash != event_hash:
                        return self._invalid_result(
                            total_events=total_events,
                            validated_events=validated_events,
                            first_invalid_sequence=line_number,
                            error_code="INTEGRITY",
                            error_message="Event hash mismatch for canonical record content.",
                            last_valid_hash=last_valid_hash,
                        )

                    validated_events += 1
                    last_valid_hash = event_hash
                    expected_previous_hash = event_hash
        except OSError as exc:
            return self._invalid_result(
                total_events=total_events,
                validated_events=validated_events,
                first_invalid_sequence=validated_events + 1,
                error_code="PERSISTENCE",
                error_message=str(exc),
                last_valid_hash=last_valid_hash,
            )

        return AuditVerificationResult(
            is_valid=True,
            total_events=total_events,
            validated_events=validated_events,
            first_invalid_sequence=None,
            error_code=None,
            error_message=None,
            last_valid_hash=last_valid_hash,
        )

    def get_last_hash(self) -> str:
        """Return genesis hash for empty file or last event hash for populated file.

        Returns:
            Current chain tail hash.

        """
        records = self.iter_records()
        if not records:
            return GENESIS_PREVIOUS_HASH

        last_hash = records[-1].get("event_hash")
        if isinstance(last_hash, str) and AuditHasher.validate_hash_format(last_hash):
            return last_hash
        return GENESIS_PREVIOUS_HASH

    def get_last_sequence(self) -> int:
        """Return the last stored sequence number or zero for empty chain.

        Returns:
            Last persisted sequence value.

        """
        records = self.iter_records()
        if not records:
            return 0

        sequence_value = records[-1].get("sequence")
        if isinstance(sequence_value, int):
            return sequence_value
        return len(records)

    def _append_record(self, record: dict[str, object]) -> None:
        """Append a single JSON record line to the audit file.

        Args:
            record: Record dictionary to serialize and append.

        Raises:
            AuditPersistenceError: If write operation fails.

        """
        try:
            if self._path.parent and not self._path.parent.exists():
                self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
                handle.write("\n")
        except OSError as exc:
            raise AuditPersistenceError(str(exc)) from exc

    @staticmethod
    def _invalid_result(
        *,
        total_events: int,
        validated_events: int,
        first_invalid_sequence: int,
        error_code: str,
        error_message: str,
        last_valid_hash: str | None,
    ) -> AuditVerificationResult:
        """Build a standardized invalid verification result payload.

        Args:
            total_events: Total events observed at failure time.
            validated_events: Number of validated events before failure.
            first_invalid_sequence: 1-based failing sequence number.
            error_code: Stable error code.
            error_message: Human-readable error message.
            last_valid_hash: Last valid event hash before failure.

        Returns:
            Structured invalid verification result.

        """
        return AuditVerificationResult(
            is_valid=False,
            total_events=total_events,
            validated_events=validated_events,
            first_invalid_sequence=first_invalid_sequence,
            error_code=error_code,
            error_message=error_message,
            last_valid_hash=last_valid_hash,
        )


def validate() -> bool:
    """Return whether module contracts are loadable.

    Returns:
        Always ``True`` when the module can be imported.

    """
    return True


__all__ = ["GENESIS_PREVIOUS_HASH", "AuditTrailCore", "validate"]
