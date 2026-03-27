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

"""Deterministic canonicalization and hashing primitives for audit events."""

from __future__ import annotations

import hashlib
import json
import re

from src.core.audit.AuditEvent import AuditEvent

_HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class AuditHasher:
    """Provide deterministic canonicalization and SHA-256 hash computation."""

    @staticmethod
    def canonical_event_bytes(event: AuditEvent) -> bytes:
        """Serialize an event to deterministic UTF-8 canonical bytes.

        Args:
            event: Audit event to canonicalize.

        Returns:
            UTF-8 encoded canonical JSON bytes.

        """
        canonical = event.to_canonical_dict()
        serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return serialized.encode("utf-8")

    @staticmethod
    def compute_event_hash(previous_hash: str, canonical_event_bytes: bytes) -> str:
        """Compute the SHA-256 hash for a chain-linked audit event.

        Args:
            previous_hash: Previous record hash in the chain.
            canonical_event_bytes: Deterministic event bytes.

        Returns:
            Lowercase hexadecimal SHA-256 hash.

        """
        digest = hashlib.sha256()
        digest.update(previous_hash.encode("ascii"))
        digest.update(b":")
        digest.update(canonical_event_bytes)
        return digest.hexdigest()

    @staticmethod
    def validate_hash_format(hash_value: str) -> bool:
        """Validate whether a hash is a lowercase 64-character hex value.

        Args:
            hash_value: Candidate hash string.

        Returns:
            ``True`` when the hash matches SHA-256 lowercase hex format.

        """
        return _HASH_PATTERN.fullmatch(hash_value) is not None


def validate() -> bool:
    """Return whether module contracts are loadable.

    Returns:
        Always ``True`` when the module can be imported.

    """
    return True


__all__ = ["AuditHasher", "validate"]
