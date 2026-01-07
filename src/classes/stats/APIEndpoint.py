#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class APIEndpoint:
    """Stats API endpoint configuration."""
    path: str
    method: str = "GET"
    auth_required: bool = True
    rate_limit: int = 100  # requests per minute
    cache_ttl: int = 60  # seconds
