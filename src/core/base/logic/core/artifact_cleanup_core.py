#!/usr/bin/env python3
"""Minimal stub for artifact_cleanup_core used during repairs."""

from __future__ import annotations


class ArtifactCleanupCore:
    """Repair-time stub of ArtifactCleanupCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["ArtifactCleanupCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: Artifact cleanup core (conservative).

Minimal implementation to restore imports.
"""
from __future__ import annotations

from typing import List


class ArtifactCleanupCore:
    def __init__(self, patterns: List[str] | None = None) -> None:
        self.patterns = patterns or ["*.mp3", "*.mp4", "*.png", "*.log"]
        self.is_running = False

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False


__all__ = ["ArtifactCleanupCore"]
