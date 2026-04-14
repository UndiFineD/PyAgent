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

"""Replay JSONL storage implementation."""

from __future__ import annotations

import json
from pathlib import Path

from .exceptions import ReplayCorruptionError, ReplaySequenceError
from .ReplayEnvelope import ReplayEnvelope


class ReplayStore:
    """Persist and load replay envelopes by session id.

    Args:
        root_path: Root folder where replay JSONL files are persisted.

    """

    def __init__(self, *, root_path: str | Path) -> None:
        """Initialize replay store paths.

        Args:
            root_path: Root folder where replay JSONL files are persisted.

        """
        self._root_path = Path(root_path)
        self._root_path.mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        """Validate store structure assumptions.

        Raises:
            ReplayCorruptionError: If the root path is not a directory.

        """
        if not self._root_path.is_dir():
            raise ReplayCorruptionError("Replay store root path is not a directory")

    async def append_envelope(self, envelope: ReplayEnvelope) -> None:
        """Append an envelope to a session stream.

        Args:
            envelope: Envelope instance to persist.

        Raises:
            ReplaySequenceError: If the sequence number already exists.

        """
        self.validate()
        existing = await self.load_session(envelope.session_id)
        if any(item.sequence_no == envelope.sequence_no for item in existing):
            raise ReplaySequenceError(
                f"Duplicate sequence_no {envelope.sequence_no} for session '{envelope.session_id}'"
            )

        path = self._session_file(envelope.session_id)
        line = json.dumps(envelope.to_dict(), sort_keys=True, separators=(",", ":"))
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.write("\n")

    async def load_session(self, session_id: str) -> list[ReplayEnvelope]:
        """Load all envelopes for a session sorted by sequence number.

        Args:
            session_id: Session identifier.

        Returns:
            Sorted list of replay envelopes.

        Raises:
            ReplayCorruptionError: If persisted JSONL data is malformed.
            ReplaySequenceError: If duplicate sequence values are found on read.

        """
        self.validate()
        path = self._session_file(session_id)
        if not path.exists():
            return []

        items: list[ReplayEnvelope] = []
        try:
            with path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    stripped = raw_line.strip()
                    if not stripped:
                        continue
                    payload = json.loads(stripped)
                    items.append(ReplayEnvelope.from_dict(payload))
        except ReplaySequenceError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ReplayCorruptionError(f"Corrupted replay session '{session_id}'") from exc

        items.sort(key=lambda item: item.sequence_no)
        sequence_set: set[int] = set()
        for envelope in items:
            if envelope.sequence_no in sequence_set:
                raise ReplaySequenceError(f"Duplicate sequence_no {envelope.sequence_no} in session '{session_id}'")
            sequence_set.add(envelope.sequence_no)
        return items

    async def load_range(self, session_id: str, start_sequence: int, end_sequence: int) -> list[ReplayEnvelope]:
        """Load inclusive sequence range for a session.

        Args:
            session_id: Session identifier.
            start_sequence: Inclusive lower sequence bound.
            end_sequence: Inclusive upper sequence bound.

        Returns:
            Deterministic subset ordered by sequence number.

        """
        if start_sequence > end_sequence:
            return []

        loaded = await self.load_session(session_id)
        return [envelope for envelope in loaded if start_sequence <= envelope.sequence_no <= end_sequence]

    async def delete_session(self, session_id: str) -> None:
        """Delete persisted envelope stream for a session.

        Args:
            session_id: Session identifier.

        """
        path = self._session_file(session_id)
        if path.exists():
            path.unlink()

    async def session_exists(self, session_id: str) -> bool:
        """Check whether persisted envelopes exist for a session.

        Args:
            session_id: Session identifier.

        Returns:
            True if a session JSONL file exists, else False.

        """
        return self._session_file(session_id).exists()

    def _session_file(self, session_id: str) -> Path:
        """Resolve session JSONL file path.

        Args:
            session_id: Session identifier.

        Returns:
            Session-specific JSONL file path.

        """
        safe_session = "".join(char for char in session_id if char.isalnum() or char in {"-", "_"})
        return self._root_path / f"{safe_session}.jsonl"
