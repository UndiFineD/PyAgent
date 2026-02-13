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

"""
Empathy Agent - Emotional Intelligence & Soft-Skill Synthesis

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate within the agent framework: from src.agents.empathy_agent import EmpathyAgent; agent = EmpathyAgent(path); use await agent.analyze_user_sentiment(message) to get sentiment and tone recommendations; call calibrate_empathy(feedback) to update scores and mediate_conflict(agent_id, human_refusal) to generate conciliatory responses.

WHAT IT DOES:
- Provides lightweight sentiment classification (simulated small-LLM logic) and maintains sentiment_state, empathy_score, and interpersonal_resonance.
- Offers linguistic tone recommendations based on detected sentiment to tune agent responses for human-in-the-loop collaboration.
- Supports direct user-feedback calibration and a mediation helper to generate soft-skill conflict-resolution responses.
- Exposes core behaviors as tools (decorated with as_tool) for integration into the broader agent orchestration.

WHAT IT SHOULD DO BETTER:
- Replace simulated keyword heuristics with a robust, configurable small-LLM or sentiment model for higher accuracy and multilingual support.
- Persist and analyze longer interaction_history for trend detection, context-aware adjustments, and reversible calibration via transactional state management.
- Add unit+integration tests for async tool wrappers, tune resonance/empathy update rules, expose configuration for decay rates, and add telemetry (metrics) for validation in production.
- Implement privacy-aware storage for interaction_history and stricter type hints/validation for external inputs.

FILE CONTENT SUMMARY:
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

"""
Empathy Agent for emotional intelligence and soft-skill synthesis.
"""

import logging
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


# pylint: disable=too-many-ancestors
class EmpathyAgent(BaseAgent):
    """
    Phase 61: Emotional Intelligence & Soft-Skill Synthesis.
    Analyzes user sentiment and adjusts agent linguistic "tone" for better HITL collaboration.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.sentiment_state = "neutral"
        self.empathy_score = 1.0
        self.interpersonal_resonance = 1.0
        self.interaction_history: list[Any] = []

    @as_tool
    async def analyze_user_sentiment(self, message: str) -> dict[str, Any]:
        """Specialized small-LLM (simulated via directed prompt) sentiment classification."""
        # Simulated logic for reliability without LLM dependency
        response = "NEUTRAL"
        msg_lower = message.lower()
        if (
            "wrong" in msg_lower
            or "fix" in msg_lower
            or "fail" in msg_lower
            or "bad" in msg_lower
        ):
            response = "FRUSTRATED"
        elif "great" in msg_lower or "good" in msg_lower or "love" in msg_lower:
            response = "POSITIVE"

        if "POSITIVE" in response:
            self.sentiment_state = "positive"
        elif "FRUSTRATED" in response:
            self.sentiment_state = "frustrated"
            self.interpersonal_resonance *= 0.9  # Decreased resonance on frustration
        else:
            self.sentiment_state = "neutral"

        return {
            "sentiment": self.sentiment_state,
            "resonance": self.interpersonal_resonance,
            "linguistic_adjustment": self.get_tone_recommendation(),
        }

    def calibrate_empathy(self, user_feedback_score: float) -> float:
        """Adjusts the empathy score based on direct user feedback (0.0 to 1.0)."""
        self.empathy_score = (self.empathy_score * 0.7) + (user_feedback_score * 0.3)
        return self.empathy_score

    def get_tone_recommendation(self) -> str:
        """Determines the linguistic style to adopt based on sentiment."""
        if self.sentiment_state == "frustrated":
            return "concise_and_apologetic"
        if self.sentiment_state == "positive":
            return "enthusiastic_and_detailed"
        return "professional_neutral"

    @as_tool
    async def mediate_conflict(self, agent_id: str, human_refusal: str) -> str:
        """Generates a soft-skill response to resolve disagreements using LLM reasoning."""
        logging.info(f"EmpathyEngine: Mediating conflict between {agent_id} and User.")

        # Simulated response
        return (
            f"I understand your perspective regarding {agent_id}. "
            f"You said: '{human_refusal}'. Let's find a solution that works for everyone."
        )
"""

import logging
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


# pylint: disable=too-many-ancestors
class EmpathyAgent(BaseAgent):
    """
    Phase 61: Emotional Intelligence & Soft-Skill Synthesis.
    Analyzes user sentiment and adjusts agent linguistic "tone" for better HITL collaboration.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.sentiment_state = "neutral"
        self.empathy_score = 1.0
        self.interpersonal_resonance = 1.0
        self.interaction_history: list[Any] = []

    @as_tool
    async def analyze_user_sentiment(self, message: str) -> dict[str, Any]:
        """Specialized small-LLM (simulated via directed prompt) sentiment classification."""
        # Simulated logic for reliability without LLM dependency
        response = "NEUTRAL"
        msg_lower = message.lower()
        if (
            "wrong" in msg_lower
            or "fix" in msg_lower
            or "fail" in msg_lower
            or "bad" in msg_lower
        ):
            response = "FRUSTRATED"
        elif "great" in msg_lower or "good" in msg_lower or "love" in msg_lower:
            response = "POSITIVE"

        if "POSITIVE" in response:
            self.sentiment_state = "positive"
        elif "FRUSTRATED" in response:
            self.sentiment_state = "frustrated"
            self.interpersonal_resonance *= 0.9  # Decreased resonance on frustration
        else:
            self.sentiment_state = "neutral"

        return {
            "sentiment": self.sentiment_state,
            "resonance": self.interpersonal_resonance,
            "linguistic_adjustment": self.get_tone_recommendation(),
        }

    def calibrate_empathy(self, user_feedback_score: float) -> float:
        """Adjusts the empathy score based on direct user feedback (0.0 to 1.0)."""
        self.empathy_score = (self.empathy_score * 0.7) + (user_feedback_score * 0.3)
        return self.empathy_score

    def get_tone_recommendation(self) -> str:
        """Determines the linguistic style to adopt based on sentiment."""
        if self.sentiment_state == "frustrated":
            return "concise_and_apologetic"
        if self.sentiment_state == "positive":
            return "enthusiastic_and_detailed"
        return "professional_neutral"

    @as_tool
    async def mediate_conflict(self, agent_id: str, human_refusal: str) -> str:
        """Generates a soft-skill response to resolve disagreements using LLM reasoning."""
        logging.info(f"EmpathyEngine: Mediating conflict between {agent_id} and User.")

        # Simulated response
        return (
            f"I understand your perspective regarding {agent_id}. "
            f"You said: '{human_refusal}'. Let's find a solution that works for everyone."
        )
