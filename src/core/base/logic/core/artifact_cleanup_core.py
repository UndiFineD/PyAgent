#!/usr/bin/env python3
"""Minimal Artifact Cleanup core for tests."""
from __future__ import annotations



try:
    from typing import List
except ImportError:
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
