#!/usr/bin/env python3
"""Minimal APT simulation core for tests."""
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


@dataclass
class APTSimulationResult:
    group: APTGroup
    success: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


class APTSimulationCore:
    def __init__(self) -> None:
        pass

    def run(self, group: APTGroup, c2: C2Profile) -> APTSimulationResult:
        return APTSimulationResult(group=group, success=False)


__all__ = ["APTGroup", "C2Profile", "APTSimulationResult", "APTSimulationCore"]
