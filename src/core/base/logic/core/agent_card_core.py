#!/usr/bin/env python3
from __future__ import annotations
"""
Parser-safe stub: Agent Card core (conservative).

Minimal, side-effect free stub preserving exported symbols for tests.
Backups are saved as `.manual_fix.bak`.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AgentCapability:
    name: str
    description: str = ""


@dataclass
class AgentCard:
    id: str
    title: str
    capabilities: List[AgentCapability] = None


class AgentCardCore:
    def __init__(self) -> None:
        self._cards: Dict[str, AgentCard] = {}

    def register_card(self, card: AgentCard) -> None:
        self._cards[card.id] = card


__all__ = ["AgentCapability", "AgentCard", "AgentCardCore"]
