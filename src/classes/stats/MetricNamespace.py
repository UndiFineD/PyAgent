#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class MetricNamespace:
    """Namespace for organizing metrics."""
    name: str
    description: str = ""
    parent: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=lambda: {})
    retention_days: int = 30
