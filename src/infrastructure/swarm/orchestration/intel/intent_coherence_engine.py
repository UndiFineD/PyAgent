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
from src.core.base.Version import VERSION
import logging
from typing import Any, TYPE_CHECKING
from datetime import datetime

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager


class IntentCoherenceEngine:
    """
    Implements Swarm Consciousness (Phase 30).
    Maintains a unified 'Intent' layer that synchronizes all agent goals
    without necessitating explicit task decomposition.
    """

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.global_intent: str | None = None
        self.intent_priority: int = 0
        self.sub_intents: list[dict[str, Any]] = []

    def broadcast_intent(self, intent: str, priority: int = 10) -> dict[str, Any]:
        """
        Sets the global coherent objective for the entire swarm.
        """
        logging.info(f"IntentCoherenceEngine: Broadcasting global intent: {intent}")
        self.global_intent = intent
        self.intent_priority = priority

        # Emit signal via the signal bus
        if hasattr(self.fleet, "signals"):
            self.fleet.signals.emit(
                "COHERENT_INTENT_ESTABLISHED",
                {
                    "intent": intent,
                    "priority": priority,
                    "timestamp": datetime.now().isoformat(),
                },
                sender="IntentCoherenceEngine",
            )

        return {
            "status": "synchronized",
            "global_intent": self.global_intent,
            "priority": self.intent_priority,
        }

    def align_agent(self, agent_name: str, local_task: str) -> str:
        """
        Re-aligns an agent's local task with the global coherent intent.
        """
        if not self.global_intent:
            return local_task

        logging.info(
            f"IntentCoherenceEngine: Aligning {agent_name} with global intent."
        )

        # In a real implementation, we'd use an LLM or vector similarity to
        # project the local task into the global intent space.

        # For simulation, we'll just prepend the global context
        aligned_task = f"[Aligned with: {self.global_intent}] {local_task}"
        return aligned_task

    def get_current_intent(self) -> str | None:
        return self.global_intent
