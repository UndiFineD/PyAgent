#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

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
