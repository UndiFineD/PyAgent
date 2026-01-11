#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass
from pathlib import Path


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class StatsBackup:
    """A persisted backup entry for StatsBackupManager."""

    name: str
    path: Path
    timestamp: str
