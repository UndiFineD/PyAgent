#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass, field
from typing import Dict


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class FederatedSource:
    """A source repository for stats federation."""
    repo_url: str
    api_endpoint: str
    auth_token: str = ""
    poll_interval_seconds: int = 300
    enabled: bool = True
    metrics: Dict[str, float] = field(default_factory=dict)
