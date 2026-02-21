#!/usr/bin/env python3
"""Minimal stub for agent_card_core used during repairs."""

from __future__ import annotations


class AgentCardCore:
    """Repair-time stub of AgentCardCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["AgentCardCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: Agent Card core (conservative).

Minimal, side-effect free stub preserving exported symbols for tests.
Backups are saved as `.manual_fix.bak`.
"""
from __future__ import annotations

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
