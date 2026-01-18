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
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION


class PersonalityCoreAgent(BaseAgent):
    """
    Manages the 'emotional intelligence' and 'vibes' of the fleet.
    Adjusts communication style and task priorities based on user context.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Fleet Personality Core. "
            "Your job is to detect the user's emotional state, urgency, and technical level. "
            "You broadcast 'vibe' signals that other agents use to adjust their tone and depth."
        )
        self.current_vibe = "neutral"

    @as_tool
    def set_vibe_track(self, user_input: str) -> dict[str, Any]:
        """
        Analyzes user input and sets the fleet-wide emotional/operational vibe.
        """
        logging.info(f"PersonalityCoreAgent: Analyzing vibe for: {user_input[:50]}...")

        # In a real implementation, we'd use LLM to classify sentiment/urgency
        # prompt = f"Analyze setiment/urgency of: {user_input}"
        # analysis = self.think(prompt)

        # Simulated analysis logic
        vibe = "professional"
        urgency = "low"

        if any(
            word in user_input.lower()
            for word in ["urgent", "asap", "emergency", "broken"]
        ):
            urgency = "high"
            vibe = "rapid_response"
        elif any(
            word in user_input.lower() for word in ["thanks", "great", "awesome", "fun"]
        ):
            vibe = "friendly"

        self.current_vibe = vibe

        # Emit signal to the fleet
        if hasattr(self, "registry") and self.registry:
            self.registry.emit(
                "FLEET_VIBE_CHANGED",
                {"vibe": vibe, "urgency": urgency, "context": user_input[:100]},
            )

        return {"status": "success", "detected_vibe": vibe, "urgency": urgency}

    @as_tool
    def get_track_guidance(self) -> str:
        """
        Returns instructions for other agents on how to behave under the current vibe.
        """
        guidance = {
            "professional": "Direct, technical, and concise.",
            "friendly": "Encouraging, helpful, and personable.",
            "rapid_response": "Extremely concise, focusing on immediate fixes and safety.",
        }
        return guidance.get(
            self.current_vibe, "Maintain standard operational parameters."
        )
