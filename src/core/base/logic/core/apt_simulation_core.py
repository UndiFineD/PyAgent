#!/usr/bin/env python3
"""Minimal stub for apt_simulation_core used during repairs."""

from __future__ import annotations


class APTSimulationCore:
    """Repair-time stub of APTSimulationCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["APTSimulationCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: APT simulation core (conservative).

Provides minimal classes used by imports/tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class APTGroup:
    name: str
    techniques: List[str] = field(default_factory=list)


@dataclass
class C2Profile:
    name: str
    endpoint: str


class APTSimulationCore:
    def run(self, group: APTGroup, c2: C2Profile):
        return None


        __all__ = ["APTGroup", "C2Profile", "APTSimulationCore"]
