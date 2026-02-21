#!/usr/bin/env python3
"""Parser-safe stub for change_monitoring_agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ChangeMonitoringAgent:
    """Minimal stub to keep imports/tests working while repo is being repaired."""

    name: str = "change_monitoring_agent"

    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - stub
        self._meta: Dict[str, Any] = {}

    def start(self) -> None:  # pragma: no cover - stub
        return None


__all__ = ["ChangeMonitoringAgent"]
