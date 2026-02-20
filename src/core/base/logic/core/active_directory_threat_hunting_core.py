#!/usr/bin/env python3
"""Minimal Active Directory threat hunting core for tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ADObjectType(Enum):
    USER = "user"
    COMPUTER = "computer"
    GROUP = "group"


@dataclass
class ADObject:
    distinguished_name: str
    object_type: ADObjectType
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatFinding:
    object_dn: str
    level: ThreatLevel
    description: str = ""


@dataclass
class HuntingResult:
    findings: List[ThreatFinding] = field(default_factory=list)


class ActiveDirectoryThreatHuntingCore:
    async def hunt(self) -> HuntingResult:
        return HuntingResult()
