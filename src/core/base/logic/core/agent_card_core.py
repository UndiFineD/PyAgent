#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AgentCapability(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    returns: str = "Any"

class AgentCard(BaseModel):
    """
    Standardized manifest for cross-agent discovery.
    Pattern harvested from agentic_design_patterns.
    """
    agent_id: str
    name: str
    version: str = "1.0.0"
    role: str
    description: str
    capabilities: List[AgentCapability] = Field(default_factory=list)
    contact_info: Dict[str, str] = Field(default_factory=dict) # e.g., {"protocol": "voyager_p2p", "address": "peer_id"}
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentCardCore:
    """
    Manages a registry of AgentCards for inter-agent communication (A2A).
    """
    def __init__(self):
        self.registry: Dict[str, AgentCard] = {}

    def register_agent(self, card: AgentCard):
        self.registry[card.agent_id] = card

    def find_agents_by_capability(self, capability_query: str) -> List[AgentCard]:
        """Finds agents that have a specific capability."""
        matches = []
        for card in self.registry.values():
            for cap in card.capabilities:
                if capability_query.lower() in cap.name.lower() or capability_query.lower() in cap.description.lower():
                    matches.append(card)
                    break
        return matches

    def get_agent_manifest(self, agent_id: str) -> Optional[AgentCard]:
        return self.registry.get(agent_id)

    def export_all_cards(self) -> List[Dict[str, Any]]:
        return [card.model_dump() for card in self.registry.values()]
