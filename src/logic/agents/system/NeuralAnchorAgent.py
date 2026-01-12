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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import logging
import json
import re
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool


class NeuralAnchorAgent(BaseAgent):
    """
    Agent responsible for anchoring reasoning to verified external sources of truth.
    Validates agent statements against documentation, specifications, and issues.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.anchors: Dict[str, Any] = {}
        self._system_prompt = (
            "You are the Neural Anchor Agent. "
            "Your mission is to prevent hallucination by strictly grounding agent reasoning in verified sources. "
            "You validate claims against documentation, specs, and previous execution logs."
        )

    @as_tool
    def load_anchor_source(self, source_name: str, content: str, source_type: str = "doc") -> str:
        """
        Registers a verified source of truth to be used for anchoring.
        """
        self.anchors[source_name] = {
            "content": content,
            "type": source_type,
            "verified": True
        }
        return f"Source '{source_name}' loaded as an anchor."

    @as_tool
    def validate_claim(self, claim: str, context_sources: List[str]) -> Dict[str, Any]:
        """
        Validates a specific claim against the loaded anchor sources.
        """
        results = []
        for src in context_sources:
            if src in self.anchors:
                anchor = self.anchors[src]
                # Simple keyword/regex check for validation in this stub
                findings = []
                keywords = re.findall(r'\b\w+\b', claim.lower())
                matches = [k for k in keywords if k in anchor["content"].lower()]
                
                score = len(matches) / len(keywords) if keywords else 0
                results.append({
                    "source": src,
                    "overlap_score": score,
                    "confidence": "High" if score > 0.5 else "Low"
                })
        
        grounded = any(r["overlap_score"] > 0.1 for r in results)
        return {
            "claim": claim,
            "is_grounded": grounded,
            "validations": results
        }

    @as_tool
    def anchor_reasoning_step(self, reasoning_chain: List[str], sources: List[str]) -> List[Dict[str, Any]]:
        """
        Iteratively validates a chain of reasoning steps.
        """
        return [self.validate_claim(step, sources) for step in reasoning_chain]
