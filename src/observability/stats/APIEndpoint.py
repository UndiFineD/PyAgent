#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class APIEndpoint:
    """Stats API endpoint configuration."""
    path: str
    method: str = "GET"
    auth_required: bool = True
    rate_limit: int = 100  # requests per minute
    cache_ttl: int = 60  # seconds
