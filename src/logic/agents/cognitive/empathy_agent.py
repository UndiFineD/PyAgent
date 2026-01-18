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
from src.core.base.version import VERSION
import logging
from typing import Dict, Any
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION

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
        self.interaction_history = []

    def analyze_user_sentiment(self, message: str) -> dict[str, Any]:
        """Specialized small-LLM (simulated via directed prompt) sentiment classification."""
        prompt = (
            f"Classify the sentiment of the following message: '{message}'\n"
            "Respond with ONLY one word: POSITIVE, FRUSTRATED, or NEUTRAL."
        )
        
        try:
            # Use self.think() for specialized classification
            response = self.think(prompt).strip().upper()
            if "POSITIVE" in response:
                self.sentiment_state = "positive"
            elif "FRUSTRATED" in response:
                self.sentiment_state = "frustrated"
                self.interpersonal_resonance *= 0.9 # Decreased resonance on frustration
            else:
                self.sentiment_state = "neutral"
        except Exception:
            self.sentiment_state = "neutral"
            
        return {
            "sentiment": self.sentiment_state,
            "resonance": self.interpersonal_resonance,
            "linguistic_adjustment": self.get_tone_recommendation()
        }

    def calibrate_empathy(self, user_feedback_score: float) -> float:
        """Adjusts the empathy score based on direct user feedback (0.0 to 1.0)."""
        self.empathy_score = (self.empathy_score * 0.7) + (user_feedback_score * 0.3)
        return self.empathy_score

    def get_tone_recommendation(self) -> str:
        """Determines the linguistic style to adopt based on sentiment."""
        if self.sentiment_state == "frustrated":
            return "concise_and_apologetic"
        elif self.sentiment_state == "positive":
            return "enthusiastic_and_detailed"
        return "professional_neutral"

    def mediate_conflict(self, agent_id: str, human_refusal: str) -> str:
        """Generates a soft-skill response to resolve disagreements using LLM reasoning."""
        logging.info(f"EmpathyEngine: Mediating conflict between {agent_id} and User.")
        
        prompt = (
            f"The agent {agent_id} proposed a change, but the user refused saying: '{human_refusal}'. "
            "Generate a supportive, non-confrontational response that acknowledges the user's concern "
            "and explores alternative solutions. Be empathetic and professional."
        )
        
        return self.think(prompt)