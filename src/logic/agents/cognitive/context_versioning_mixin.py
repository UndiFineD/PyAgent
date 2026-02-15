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

# Licensed under the Apache License, Version 2.0 (the "License");


"""
Context Versioning Mixin - Context snapshotting and compression

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Inherit into a ContextAgent-like class.
- Use create_version(version, changes, author) to snapshot current/previous content.
- Use compress_content()/decompress_content() to store/retrieve compressed payloads.
- Use get_versions(), get_latest_version(), get_version_diff(v1, v2), get_compression_ratio() for queries and metrics.

WHAT IT DOES:
- Computes short SHA-256 content hashes for snapshots and records version metadata.
- Keeps an in-memory list of ContextVersion objects (_versions).
- Provides zlib-based compression/decompression and a simple compression-ratio metric.
- Exposes a diff-like summary comparing two stored version hashes and change lists.

WHAT IT SHOULD DO BETTER:
- Persist versions and compressed blobs to durable storage (DB or object store) instead of in-memory _versions/_compressed_content.
- Handle empty or non-text content robustly and surface clear exceptions on encode/decode failures.
- Make compression per-version (not a single _compressed_content), add version->blob mapping, and avoid overwriting compressed state.
- Improve timezones/formatting for timestamps, stronger typing and validation, and add thread-safety for concurrent agents.
- Add unit tests for edge cases, and allow configurable compression level and hash length.

FILE CONTENT SUMMARY:
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

# Licensed under the Apache License, Version 2.0 (the "License");


"""Mixin for context versioning and snapshotting."""

from __future__ import annotations
import hashlib
import logging
import zlib
from datetime import datetime
from typing import Any
from src.logic.agents.cognitive.context.models.context_version import ContextVersion


class ContextVersioningMixin:
    """Versioning and compression methods for ContextAgent."""

    def create_version(
        self, version: str, changes: list[str] | None = None, author: str = ""
    ) -> ContextVersion:
        """Create a new version snapshot."""
        content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

        version_obj = ContextVersion(
            version=version,
            timestamp=datetime.now().isoformat(),
            content_hash=content_hash,
            changes=changes or [],
            author=author,
        )

        if not hasattr(self, "_versions"):
            self._versions: list[ContextVersion] = []
        self._versions.append(version_obj)
        logging.info(f"Created version {version}")
        return version_obj

    def get_versions(self) -> list[ContextVersion]:
        """Get all versions."""
        return getattr(self, "_versions", [])

    def get_latest_version(self) -> ContextVersion | None:
        """Get the latest version."""
        versions = getattr(self, "_versions", [])
        return versions[-1] if versions else None

    def get_version_diff(self, v1: str, v2: str) -> dict[str, Any]:
        """Get diff between two versions."""
        versions = getattr(self, "_versions", [])
        ver1 = next((v for v in versions if v.version == v1), None)
        ver2 = next((v for v in versions if v.version == v2), None)

        if not ver1 or not ver2:
            return {"error": "Version not found"}

        return {
            "from_version": v1,
            "to_version": v2,
            "from_hash": ver1.content_hash,
            "to_hash": ver2.content_hash,
            "changed": ver1.content_hash != ver2.content_hash,
            "changes_v2": ver2.changes,
        }

    def compress_content(self, content: str | None = None) -> bytes:
        """Compress content for storage."""
        if content is None:
            content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")

        self._compressed_content = zlib.compress(content.encode(), level=9)
        return self._compressed_content

    def decompress_content(self, compressed: bytes | None = None) -> str:
        """Decompress stored content."""
        if compressed is None:
            compressed = getattr(self, "_compressed_content", None)

        if compressed is None:
            return ""

        return zlib.decompress(compressed).decode()

    def get_compression_ratio(self, content: str | None = None) -> float:
        """Get compression ratio (space savings) for the current/previous content."""
        if content is None:
            content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")

        original_size = len(content.encode())
        if original_size == 0:
            return 0.0

        compressed = getattr(self, "_compressed_content", None)
        if compressed is None:
            compressed = self.compress_content(content)
        compressed_size = len(compressed)
        return 1 - (compressed_size / original_size)
"""

from __future__ import annotations
import hashlib
import logging
import zlib
from datetime import datetime
from typing import Any
from src.logic.agents.cognitive.context.models.context_version import ContextVersion


class ContextVersioningMixin:
    """Versioning and compression methods for ContextAgent."""

    def create_version(
        self, version: str, changes: list[str] | None = None, author: str = ""
    ) -> ContextVersion:
        """Create a new version snapshot."""
        content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

        version_obj = ContextVersion(
            version=version,
            timestamp=datetime.now().isoformat(),
            content_hash=content_hash,
            changes=changes or [],
            author=author,
        )

        if not hasattr(self, "_versions"):
            self._versions: list[ContextVersion] = []
        self._versions.append(version_obj)
        logging.info(f"Created version {version}")
        return version_obj

    def get_versions(self) -> list[ContextVersion]:
        """Get all versions."""
        return getattr(self, "_versions", [])

    def get_latest_version(self) -> ContextVersion | None:
        """Get the latest version."""
        versions = getattr(self, "_versions", [])
        return versions[-1] if versions else None

    def get_version_diff(self, v1: str, v2: str) -> dict[str, Any]:
        """Get diff between two versions."""
        versions = getattr(self, "_versions", [])
        ver1 = next((v for v in versions if v.version == v1), None)
        ver2 = next((v for v in versions if v.version == v2), None)

        if not ver1 or not ver2:
            return {"error": "Version not found"}

        return {
            "from_version": v1,
            "to_version": v2,
            "from_hash": ver1.content_hash,
            "to_hash": ver2.content_hash,
            "changed": ver1.content_hash != ver2.content_hash,
            "changes_v2": ver2.changes,
        }

    def compress_content(self, content: str | None = None) -> bytes:
        """Compress content for storage."""
        if content is None:
            content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")

        self._compressed_content = zlib.compress(content.encode(), level=9)
        return self._compressed_content

    def decompress_content(self, compressed: bytes | None = None) -> str:
        """Decompress stored content."""
        if compressed is None:
            compressed = getattr(self, "_compressed_content", None)

        if compressed is None:
            return ""

        return zlib.decompress(compressed).decode()

    def get_compression_ratio(self, content: str | None = None) -> float:
        """Get compression ratio (space savings) for the current/previous content."""
        if content is None:
            content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")

        original_size = len(content.encode())
        if original_size == 0:
            return 0.0

        compressed = getattr(self, "_compressed_content", None)
        if compressed is None:
            compressed = self.compress_content(content)
        compressed_size = len(compressed)
        return 1 - (compressed_size / original_size)
