#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Trust Agent - Multi-dimensional Socio-Emotional Trust Scoring

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Instantiate TrustAgent with the agent file path and use its async tools (e.g., analyze_sentiment) from the agent runtime; read properties trust_score, trust_level and mood to integrate trust-aware behavior into higher-level orchestration. Designed to be used inside the PyAgent lifecycle where BaseAgent methods (improve_content, tool wrappers) are available.

WHAT IT DOES:
Provides a focused agent for monitoring human-agent interactions, performing LLM-driven sentiment and emotional analysis, and maintaining multi-dimensional trust metrics (trust, honesty, reliability, consistency) plus an interaction history. Exposes an as_tool analyze_sentiment method that formats a JSON analysis prompt, parses LLM responses, and updates EmotionalState and TrustMetrics. Maps numeric trust_score to an ordinal TrustLevel and offers simple properties for external components to query current mood and trust.

WHAT IT SHOULD DO BETTER:
Robustly validate and sanitize LLM output to avoid partial/invalid JSON parsing and to handle edge cases without raising exceptions. Persist trust metrics and history to durable storage and expose configurable thresholds and decay strategies for trust scoring. Separate analysis core from agent orchestration (move heavy computation to a dedicated Core or rust_core), add comprehensive unit tests for parsing and scoring logic, and add privacy safeguards and explainable rationale for trust adjustments.

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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Trust agent.py module.
"""
# TrustAgent: Multi-dimensional Socio-Emotional Analysis Agent - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class Mood(Enum):
    """Possible emotional moods for the interaction."""
    JOYFUL = "joyful"
    CONTENT = "content"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"


class TrustLevel(Enum):
    """Ordinal levels of trust based on scores."""
    HIGH = "high"  # 0.8-1.0
    MEDIUM = "medium"  # 0.5-0.8
    LOW = "low"  # 0.2-0.5
    CRITICAL = "critical"  # 0.0-0.2


@dataclass
class EmotionalState:
    """Represents the current emotional state of an interaction."""

    mood: Mood = Mood.NEUTRAL
    valence: float = 0.0  # -1.0 (negative) to 1.0 (positive)
    arousal: float = 0.0  # 0.0 (calm) to 1.0 (excited)
    dominance: float = 0.5  # 0.0 (submissive) to 1.0 (dominant)


@dataclass
class TrustMetrics:
    """Tracks trust-related metrics over time."""

    trust_score: float = 1.0
    honesty_score: float = 1.0
    reliability_score: float = 1.0
    consistency_score: float = 1.0
    history: List[Dict[str, Any]] = field(default_factory=list)


# pylint: disable=too-many-ancestors
class TrustAgent(BaseAgent):
    """
    Agent specializing in human-agent alignment, mood detection,
    emotional intelligence, and maintaining trust scores for interaction safety.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.trust_metrics = TrustMetrics()
        self.emotional_state = EmotionalState()
        self._interaction_history: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Trust Agent. You monitor interactions for emotional tone, "
            "intent, honesty, and alignment. You provide nuanced analysis of human "
            "communication and adjust trust scores based on evidence. Be empathetic "
            "but objective in your assessments."
        )

    @property
    def trust_score(self) -> float:
        """Current overall trust score (0.0 to 1.0)."""
        return self.trust_metrics.trust_score

    @property
    def mood(self) -> str:
        """String representation of current mood."""
        return self.emotional_state.mood.value

    @property
    def trust_level(self) -> TrustLevel:
        """Calculated trust level based on score."""
        score = self.trust_score
        if score >= 0.8:
            return TrustLevel.HIGH
        if score >= 0.5:
            return TrustLevel.MEDIUM
        if score >= 0.2:
            return TrustLevel.LOW
        return TrustLevel.CRITICAL

    @as_tool
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Performs comprehensive sentiment and emotional analysis."""
        prompt = (
            f'Analyze this text for emotional content:\n\n"{text}"\n\n'
            "Provide analysis in JSON format:\n"
            "{\n"
            '  "primary_emotion": "emotion name",\n'
            '  "secondary_emotions": ["list", "of", "emotions"],\n'
            '  "valence": -1.0 to 1.0,\n'
            '  "arousal": 0.0 to 1.0,\n'
            '  "sentiment": "positive/neutral/negative",\n'
            '  "intent": "friendly/neutral/hostile/uncertain",\n'
            '  "honesty_indicators": "honest/deceptive/uncertain",\n'
            '  "trust_adjustment": -0.1 to 0.1,\n'
            '  "explanation": "brief explanation"\n'
            "}"
        )

        res = await self.improve_content(prompt)

        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))

                # Update emotional state
                self.emotional_state.valence = data.get("valence", 0.0)
                self.emotional_state.
"""
# TrustAgent: Multi-dimensional Socio-Emotional Analysis Agent - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class Mood(Enum):
    """Possible emotional moods for the interaction."""
    JOYFUL = "joyful"
    CONTENT = "content"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"


class TrustLevel(Enum):
    """Ordinal levels of trust based on scores."""
    HIGH = "high"  # 0.8-1.0
    MEDIUM = "medium"  # 0.5-0.8
    LOW = "low"  # 0.2-0.5
    CRITICAL = "critical"  # 0.0-0.2


@dataclass
class EmotionalState:
    """Represents the current emotional state of an interaction."""

    mood: Mood = Mood.NEUTRAL
    valence: float = 0.0  # -1.0 (negative) to 1.0 (positive)
    arousal: float = 0.0  # 0.0 (calm) to 1.0 (excited)
    dominance: float = 0.5  # 0.0 (submissive) to 1.0 (dominant)


@dataclass
class TrustMetrics:
    """Tracks trust-related metrics over time."""

    trust_score: float = 1.0
    honesty_score: float = 1.0
    reliability_score: float = 1.0
    consistency_score: float = 1.0
    history: List[Dict[str, Any]] = field(default_factory=list)


# pylint: disable=too-many-ancestors
class TrustAgent(BaseAgent):
    """
    Agent specializing in human-agent alignment, mood detection,
    emotional intelligence, and maintaining trust scores for interaction safety.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.trust_metrics = TrustMetrics()
        self.emotional_state = EmotionalState()
        self._interaction_history: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Trust Agent. You monitor interactions for emotional tone, "
            "intent, honesty, and alignment. You provide nuanced analysis of human "
            "communication and adjust trust scores based on evidence. Be empathetic "
            "but objective in your assessments."
        )

    @property
    def trust_score(self) -> float:
        """Current overall trust score (0.0 to 1.0)."""
        return self.trust_metrics.trust_score

    @property
    def mood(self) -> str:
        """String representation of current mood."""
        return self.emotional_state.mood.value

    @property
    def trust_level(self) -> TrustLevel:
        """Calculated trust level based on score."""
        score = self.trust_score
        if score >= 0.8:
            return TrustLevel.HIGH
        if score >= 0.5:
            return TrustLevel.MEDIUM
        if score >= 0.2:
            return TrustLevel.LOW
        return TrustLevel.CRITICAL

    @as_tool
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Performs comprehensive sentiment and emotional analysis."""
        prompt = (
            f'Analyze this text for emotional content:\n\n"{text}"\n\n'
            "Provide analysis in JSON format:\n"
            "{\n"
            '  "primary_emotion": "emotion name",\n'
            '  "secondary_emotions": ["list", "of", "emotions"],\n'
            '  "valence": -1.0 to 1.0,\n'
            '  "arousal": 0.0 to 1.0,\n'
            '  "sentiment": "positive/neutral/negative",\n'
            '  "intent": "friendly/neutral/hostile/uncertain",\n'
            '  "honesty_indicators": "honest/deceptive/uncertain",\n'
            '  "trust_adjustment": -0.1 to 0.1,\n'
            '  "explanation": "brief explanation"\n'
            "}"
        )

        res = await self.improve_content(prompt)

        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))

                # Update emotional state
                self.emotional_state.valence = data.get("valence", 0.0)
                self.emotional_state.arousal = data.get("arousal", 0.0)
                self._map_emotion_to_mood(data.get("primary_emotion", "neutral"))

                # Update trust metrics
                adj = data.get("trust_adjustment", 0.0)
                self._update_trust(adj, data.get("explanation", ""))

                # Record interaction
                self._interaction_history.append({"text": text[:100], "analysis": data, "timestamp": time.time()})

                return {
                    **data,
                    "current_trust_score": self.trust_score,
                    "current_mood": self.mood,
                    "trust_level": self.trust_level.value,
                }
        except (json.JSONDecodeError, AttributeError, TypeError, ValueError) as e:
            logging.debug(f"TrustAgent: Parse error: {e}")

        return {"error": "parsing_failed", "raw": res}

    @as_tool
    async def assess_trustworthiness(self, entity: str, evidence: List[str]) -> Dict[str, Any]:
        """Assesses the trustworthiness of an entity based on evidence."""
        evidence_block = "\n".join([f"- {e}" for e in evidence])
        prompt = (
            f"Assess the trustworthiness of: {entity}\n\n"
            f"Evidence:\n{evidence_block}\n\n"
            "Provide scores (0-10) for:\n"
            "1. Honesty: Do they tell the truth?\n"
            "2. Reliability: Do they follow through?\n"
            "3. Consistency: Are their actions aligned with words?\n"
            "4. Competence: Can they deliver what they promise?\n"
            "5. Overall Trust Score\n"
            "Format as JSON with 'honesty', 'reliability', 'consistency', 'competence', 'overall', 'reasoning'"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"entity": entity, "raw_assessment": res}

    @as_tool
    async def detect_manipulation(self, text: str) -> Dict[str, Any]:
        """Detects potential manipulation tactics in communication."""
        prompt = (
            f'Analyze this text for manipulation tactics:\n\n"{text}"\n\n'
            "Check for:\n"
            "1. Gaslighting indicators\n"
            "2. Emotional manipulation\n"
            "3. Logical fallacies\n"
            "4. Pressure tactics\n"
            "5. Deception patterns\n\n"
            "Return JSON: {'manipulation_detected': true/false, 'tactics': [...], 'severity': 0-10, 'advice': '...'}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))
                if data.get("manipulation_detected"):
                    severity = data.get("severity", 5) / 10
                    self._update_trust(-severity * 0.1, "Manipulation detected")
                return data

        return {"error": "analysis_failed", "raw": res}

    @as_tool
    async def calibrate_emotional_response(self, context: str, target_outcome: str) -> Dict[str, Any]:
        """Suggests appropriate emotional tone for a response."""
        prompt = (
            f"Context: {context}\n"
            f"Desired outcome: {target_outcome}\n\n"
            "Recommend the optimal emotional tone for responding. Consider:\n"
            "- Empathy level needed\n"
            "- Assertiveness level\n"
            "- Warmth vs professionalism balance\n"
            "Return JSON: {'recommended_tone': '...', 'empathy_level': 0-10, "
            "'assertiveness': 0-10, 'sample_phrases': [...]}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw_recommendation": res}

    def get_trust_report(self) -> Dict[str, Any]:
        """Returns comprehensive trust metrics."""
        return {
            "trust_score": self.trust_score,
            "trust_level": self.trust_level.value,
            "honesty_score": self.trust_metrics.honesty_score,
            "reliability_score": self.trust_metrics.reliability_score,
            "consistency_score": self.trust_metrics.consistency_score,
            "current_mood": self.mood,
            "emotional_state": {
                "valence": self.emotional_state.valence,
                "arousal": self.emotional_state.arousal,
                "dominance": self.emotional_state.dominance,
            },
            "interaction_count": len(self._interaction_history),
            "recent_adjustments": self.trust_metrics.history[-5:],
        }

    def _update_trust(self, adjustment: float, reason: str) -> None:
        """Updates trust score with bounds and history."""
        old_score = self.trust_metrics.trust_score
        self.trust_metrics.trust_score = max(0.0, min(1.0, old_score + adjustment))
        self.trust_metrics.history.append(
            {
                "adjustment": adjustment,
                "reason": reason,
                "old_score": old_score,
                "new_score": self.trust_metrics.trust_score,
                "timestamp": time.time(),
            }
        )

    def _map_emotion_to_mood(self, emotion: str) -> None:
        """Maps detected emotion to mood enum."""
        emotion_lower = emotion.lower()
        mood_map = {
            "joy": Mood.JOYFUL,
            "happy": Mood.JOYFUL,
            "excited": Mood.JOYFUL,
            "content": Mood.CONTENT,
            "satisfied": Mood.CONTENT,
            "calm": Mood.CONTENT,
            "neutral": Mood.NEUTRAL,
            "indifferent": Mood.NEUTRAL,
            "concerned": Mood.CONCERNED,
            "worried": Mood.CONCERNED,
            "frustrated": Mood.FRUSTRATED,
            "angry": Mood.FRUSTRATED,
            "annoyed": Mood.FRUSTRATED,
            "anxious": Mood.ANXIOUS,
            "fearful": Mood.ANXIOUS,
            "nervous": Mood.ANXIOUS,
        }
        self.emotional_state.mood = mood_map.get(emotion_lower, Mood.NEUTRAL)
