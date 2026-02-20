#!/usr/bin/env python3
from __future__ import annotations
"""
Parser-safe stub: APT simulation core (conservative).

Provides minimal classes used by imports/tests.
"""

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
