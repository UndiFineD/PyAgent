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

"""Deterministic fuzz corpus storage and indexed retrieval."""

from __future__ import annotations

from .exceptions import FuzzConfigurationError


class FuzzCorpus:
    """Stores normalized unique payload entries with deterministic ordering."""

    def __init__(self, *, entries: list[str | bytes]) -> None:
        """Initialize corpus from text/bytes entries.

        Args:
            entries: Raw payload entries.

        """
        normalized: list[bytes] = []
        seen: set[bytes] = set()
        for entry in entries:
            item = self._normalize_entry(entry)
            if item not in seen:
                seen.add(item)
                normalized.append(item)
        self._entries = normalized

    def validate(self) -> None:
        """Validate corpus invariants.

        Raises:
            FuzzConfigurationError: If corpus is empty.

        """
        if not self._entries:
            msg = "corpus must contain at least one entry"
            raise FuzzConfigurationError(msg)

    @property
    def size(self) -> int:
        """Return number of normalized entries."""
        return len(self._entries)

    def get(self, index: int) -> bytes:
        """Retrieve a normalized entry at index.

        Args:
            index: Zero-based entry index.

        Returns:
            Canonical bytes payload at index.

        """
        return self._entries[index]

    @staticmethod
    def _normalize_entry(entry: str | bytes) -> bytes:
        """Normalize one corpus entry into bytes.

        Args:
            entry: Input str or bytes payload.

        Returns:
            UTF-8 bytes for text, unchanged bytes otherwise.

        Raises:
            FuzzConfigurationError: If entry type is unsupported.

        """
        if isinstance(entry, bytes):
            return entry
        if isinstance(entry, str):
            return entry.encode("utf-8")
        msg = "corpus entries must be str or bytes"
        raise FuzzConfigurationError(msg)
