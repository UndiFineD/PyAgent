#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ABComparison:
    """A / B comparison between code versions."""
    id: str
    version_a: str
    version_b: str
    metrics_a: Dict[str, float] = field(default_factory=lambda: {})
    metrics_b: Dict[str, float] = field(default_factory=lambda: {})
    winner: str = ""
    confidence: float = 0.0
