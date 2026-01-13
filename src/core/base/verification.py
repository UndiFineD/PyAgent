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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Verification logic for agent outputs.
Implements Stanford Reseach 'Anchoring Strength' and Keio University 'Self-Verification' paths.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any, Dict

__version__ = VERSION

class AgentVerifier:
    """Handles quality and anchoring verification of agent responses."""

    @staticmethod
    def calculate_anchoring_strength(result: str, context_pool: Dict[str, Any]) -> float:
        """
        Calculates the 'Anchoring Strength' metric.
        Measures how well the output is anchored to the provided context/grounding.
        """
        if not context_pool:
            return 0.5
            
        context_text = " ".join([str(v) for v in context_pool.values()])
        if not context_text:
            return 0.5
            
        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0
            
        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)
        
        if len(result_words) < 5:
            score *= 0.5
            
        return min(1.0, score * 1.5)

    @staticmethod
    def verify_self(result: str, anchoring_score: float) -> tuple[bool, str]:
        """Self-verification layer output check."""
        if not result:
            return False, "Empty result"
            
        hallucination_threshold = 0.3
        if anchoring_score < hallucination_threshold:
            return False, f"Low anchoring strength ({anchoring_score:.2f})"
            
        return True, "Verified"