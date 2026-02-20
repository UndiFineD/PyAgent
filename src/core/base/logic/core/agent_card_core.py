#!/usr/bin/env python3
"""Minimal Agent Card core for tests."""
from __future__ import annotations



try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import List, Dict, Any
except ImportError:
    from typing import List, Dict, Any



@dataclass
class AgentCapability:
    name: str
    description: str = ""


@dataclass
class AgentCard:
    id: str
    title: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


class AgentCardCore:
    def __init__(self) -> None:
        self._cards: Dict[str, AgentCard] = {}

    def register_card(self, card: AgentCard) -> None:
        self._cards[card.id] = card

    def get_card(self, card_id: str) -> AgentCard | None:
        return self._cards.get(card_id)

    def list_cards(self) -> List[AgentCard]:
        return list(self._cards.values())


__all__ = ["AgentCapability", "AgentCard", "AgentCardCore"]
