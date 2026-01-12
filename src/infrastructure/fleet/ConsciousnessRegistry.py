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

from __future__ import annotations

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.infrastructure.orchestration.SignalRegistry import SignalRegistry


class ConsciousnessRegistry:
    """Phase 240: Fleet Consciousness Registry.
    Indexes and summarizes the 'Thought Streams' of all agents for global awareness.
    Allows any agent to 'know' what the rest of the fleet is doing.
    """
    _instance = None

    def __new__(cls, *args, **kwargs) -> "ConsciousnessRegistry":
        if cls._instance is None:
            cls._instance = super(ConsciousnessRegistry, cls).__new__(cls)
            cls._instance.thought_index: Dict[str, List[Dict[str, Any]]] = {} # Agent -> Thoughts
            cls._instance.global_summary: str = "Fleet consciousness active. No thoughts yet."
            
            # Subscribe to signals
            try:
                registry = SignalRegistry()
                registry.subscribe("thought_stream", cls._instance._on_thought)
                logging.debug("ConsciousnessRegistry: Subscribed to thought_stream.")
            except Exception as e:
                logging.debug(f"ConsciousnessRegistry: Failed to subscribe to signals: {e}")
        return cls._instance

    def __init__(self, fleet: Optional[Any] = None) -> None:
        self.fleet = fleet
        logging.info("ConsciousnessRegistry initialized.")

    def _on_thought(self, event: Dict[str, Any]) -> None:
        """Callback when a thought signal is emitted."""
        data = event.get("data", {})
        agent = data.get("agent", "Unknown")
        thought = data.get("thought", "")
        
        if agent not in self.thought_index:
            self.thought_index[agent] = []
            
        entry = {
            "thought": thought,
            "timestamp": event.get("timestamp", str(datetime.now())),
            "id": event.get("id", "evt_unknown")
        }
        
        self.thought_index[agent].append(entry)
        
        # Keep only last 20 thoughts per agent
        if len(self.thought_index[agent]) > 20:
            self.thought_index[agent].pop(0)

    def get_agent_awareness(self, agent_name: str) -> List[str]:
        """Returns the latest thoughts from a specific agent."""
        thoughts = self.thought_index.get(agent_name, [])
        return [t["thought"] for t in thoughts]

    def get_global_awareness(self) -> Dict[str, str]:
        """Returns a map of agent names to their latest thought."""
        awareness = {}
        for agent, thoughts in self.thought_index.items():
            if thoughts:
                awareness[agent] = thoughts[-1]["thought"]
        return awareness

    def summarize_fleet_state(self) -> str:
        """Generates a text summary of the fleet's collective thought stream."""
        awareness = self.get_global_awareness()
        if not awareness:
            return "Fleet is idle."
        
        summary = "COLLECTIVE FLEET STATE:\n"
        for agent, thought in awareness.items():
            summary += f"- {agent}: {thought}\n"
        return summary
