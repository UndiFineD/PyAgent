#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass, field
from typing import Dict, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MetricNamespace:
    """Namespace for organizing metrics."""
    name: str
    description: str = ""
    parent: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=lambda: {})
    retention_days: int = 30
