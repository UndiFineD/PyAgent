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
"""Refresh-session persistence for backend-managed auth sessions."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class RefreshSessionStore:
    """Persist refresh-session records with single-process locking.

    Args:
        path: Absolute or relative file path for JSON persistence.

    """

    path: Path
    _lock: asyncio.Lock = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize lock and normalize persistence path."""
        self.path = self.path.resolve()
        self._lock = asyncio.Lock()

    async def create_session(
        self,
        *,
        session_id: str,
        subject: str,
        token_family_id: str,
        refresh_token_jti: str,
        refresh_token: str,
        refresh_expires_at: int,
        access_expires_in_seconds: int,
    ) -> dict[str, Any]:
        """Create and persist a new refresh-managed session record.

        Args:
            session_id: Stable session identifier.
            subject: Subject bound to the session.
            token_family_id: Identifier for the rotation family.
            refresh_token_jti: Identifier for active refresh token instance.
            refresh_token: Opaque refresh token plaintext value.
            refresh_expires_at: Epoch timestamp when refresh expires.
            access_expires_in_seconds: Access-token TTL in seconds.

        Returns:
            dict[str, Any]: Persisted session record.

        """
        now = _utcnow_iso()
        record: dict[str, Any] = {
            "session_id": session_id,
            "subject": subject,
            "token_family_id": token_family_id,
            "current_refresh_token_hash": _hash_refresh_token(refresh_token),
            "current_refresh_token_jti": refresh_token_jti,
            "created_at": now,
            "last_rotated_at": now,
            "access_expires_in_seconds": access_expires_in_seconds,
            "refresh_expires_at": refresh_expires_at,
            "revoked_at": None,
            "revocation_reason": None,
        }
        async with self._lock:
            data = await self._read_all_unlocked()
            sessions = data.setdefault("sessions", [])
            sessions.append(record)
            await self._write_all_unlocked(data)
        return record

    async def rotate_session(
        self,
        *,
        refresh_token: str,
        next_refresh_token: str,
        next_refresh_token_jti: str,
        next_refresh_expires_at: int,
    ) -> dict[str, Any] | None:
        """Rotate refresh token when the provided token is currently active.

        Args:
            refresh_token: Current refresh token plaintext.
            next_refresh_token: New refresh token plaintext.
            next_refresh_token_jti: Identifier for the new refresh token.
            next_refresh_expires_at: Epoch timestamp when the new refresh expires.

        Returns:
            dict[str, Any] | None: Updated record when rotation succeeds, else None.

        """
        current_hash = _hash_refresh_token(refresh_token)
        now_epoch = _utcnow_epoch()
        async with self._lock:
            data = await self._read_all_unlocked()
            sessions = data.setdefault("sessions", [])
            for record in sessions:
                if record.get("current_refresh_token_hash") != current_hash:
                    continue
                if record.get("revoked_at"):
                    return None
                if int(record.get("refresh_expires_at", 0)) <= now_epoch:
                    return None
                record["current_refresh_token_hash"] = _hash_refresh_token(next_refresh_token)
                record["current_refresh_token_jti"] = next_refresh_token_jti
                record["last_rotated_at"] = _utcnow_iso()
                record["refresh_expires_at"] = next_refresh_expires_at
                await self._write_all_unlocked(data)
                return record
        return None

    async def revoke_session(self, *, refresh_token: str) -> dict[str, Any] | None:
        """Revoke one session family matched by active refresh token.

        Args:
            refresh_token: Active refresh token plaintext.

        Returns:
            dict[str, Any] | None: Revoked record when found and active, else None.

        """
        current_hash = _hash_refresh_token(refresh_token)
        now_epoch = _utcnow_epoch()
        async with self._lock:
            data = await self._read_all_unlocked()
            sessions = data.setdefault("sessions", [])
            for record in sessions:
                if record.get("current_refresh_token_hash") != current_hash:
                    continue
                if record.get("revoked_at"):
                    return None
                if int(record.get("refresh_expires_at", 0)) <= now_epoch:
                    return None
                record["revoked_at"] = _utcnow_iso()
                record["revocation_reason"] = "logout"
                await self._write_all_unlocked(data)
                return record
        return None

    async def _read_all_unlocked(self) -> dict[str, Any]:
        """Read persistence payload.

        Returns:
            dict[str, Any]: Parsed payload with a sessions list.

        """
        if not self.path.exists():
            return {"sessions": []}
        text = await asyncio.to_thread(self.path.read_text, "utf-8")
        if not text.strip():
            return {"sessions": []}
        parsed = json.loads(text)
        if isinstance(parsed, dict) and isinstance(parsed.get("sessions"), list):
            return parsed
        return {"sessions": []}

    async def _write_all_unlocked(self, data: dict[str, Any]) -> None:
        """Write persistence payload atomically.

        Args:
            data: Full payload dictionary to persist.

        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data, indent=2, sort_keys=True)

        def _write_atomic() -> None:
            """Write a file and replace the target path atomically."""
            fd, tmp_name = tempfile.mkstemp(
                prefix=f"{self.path.stem}.",
                suffix=".tmp",
                dir=str(self.path.parent),
                text=True,
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(payload)
                os.replace(tmp_name, self.path)
            finally:
                if os.path.exists(tmp_name):
                    os.unlink(tmp_name)

        await asyncio.to_thread(_write_atomic)


def _hash_refresh_token(refresh_token: str) -> str:
    """Return the SHA-256 hex digest for a refresh token.

    Args:
        refresh_token: Plaintext opaque refresh token.

    Returns:
        str: Hex digest for persistence and lookup.

    """
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def _utcnow_epoch() -> int:
    """Return current UTC epoch seconds.

    Returns:
        int: UTC timestamp in whole seconds.

    """
    return int(datetime.now(timezone.utc).timestamp())


def _utcnow_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format.

    Returns:
        str: UTC timestamp string.

    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
