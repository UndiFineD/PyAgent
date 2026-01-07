#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class StatsSubscription:
    """A subscription entry for StatsSubscriptionManager."""

    id: str
    subscriber_id: str
    metric_pattern: str
    delivery_method: str
    created_at: str
