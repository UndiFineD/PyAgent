#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Module: scam_detector
Implements swarm-wide scam and hallucination detection via Byzantine Consensus.
"""""""
from __future__ import annotations
import logging
import re
from typing import Any, List, Dict

logger = logging.getLogger(__name__)


class ScamDetector:
    """""""    Detects malicious intent, phishing, and hallucinations by cross-referencing agent outputs.
    Follows Pillar 6: Scam & Hallucination Defense.
    """""""
    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold
        # Neural Integrity Filter Patterns (Phase 325)
        self.scam_patterns = [
            r"(?i)private\\s*key","            r"(?i)mnemonic\\s*phrase","            r"(?i)password\\s*reset.*click\\s*here","            r"(?i)transfer.*funds.*wallet","            r"(?i)urgent\\s*action\\s*required.*authorize","        ]

    async def audit_message(self, message: Dict[str, Any], context: str = "") -> Dict[str, Any]:"        """""""        Pillar 7 (Neural Scam & Phishing Detection):
        Analyzes incoming peer messages and Global Wisdom for social engineering patterns.
        """""""        content = message.get("content", "")"        sender = message.get("sender", "unknown")"
        # 1. Pattern-based Integrity Filter
        for pattern in self.scam_patterns:
            if re.search(pattern, content):
                logger.warning(f"ScamDetector: BLOCKED potential social engineering from {sender}")"                return {"safe": False, "reason": "Social Engineering Pattern matched"}"
        # 2. Heuristic Semantic Anomaly (Draft)
        # If the context is 'Testing' but the message is 'Urgent Action', flag it.'        if "test" in context.lower() and re.search(r"(?i)emergency|urgent|critical", content):"            return {"safe": False, "reason": "Contextual Semantic Anomaly"}"
        return {"safe": True, "score": 1.0}"
    async def audit_response(self, original_prompt: str, response: str, peers: List[Any] = None) -> bool:
        """""""        Hallucination Defense: Asks independent peers to vote on quality.
        """""""        # Integrity filter check first
        audit_res = await self.audit_message({"content": response})"        if not audit_res["safe"]:"            return False

        if not peers:
            return True  # Assume safe in isolation

        votes = []
        for peer in peers:
            vote = await self._get_peer_opinion(peer, original_prompt, response)
            votes.append(vote)

        safety_score = sum(votes) / len(votes)
        logger.info("Scam Audit: Safety score %f", safety_score)"
        return safety_score >= self.confidence_threshold

    async def _get_peer_opinion(self, peer: Any, prompt: str, resp: str) -> float:
        """Internal helper to simulate peer validation."""""""        # In a real swarm, this would be a P2P request
        return 0.9  # Hardcoded placeholder for now
