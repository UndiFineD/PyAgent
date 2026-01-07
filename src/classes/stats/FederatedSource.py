#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class FederatedSource:
    """A source repository for stats federation."""
    repo_url: str
    api_endpoint: str
    auth_token: str = ""
    poll_interval_seconds: int = 300
    enabled: bool = True
