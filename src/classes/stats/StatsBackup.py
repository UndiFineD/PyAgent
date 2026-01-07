#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass
class StatsBackup:
    """A persisted backup entry for StatsBackupManager."""

    name: str
    path: Path
    timestamp: str
