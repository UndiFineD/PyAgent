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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import re
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class NeuroSymbolicAgent(BaseAgent):
    """
    Phase 36: Neuro-Symbolic Reasoning.
    Verifies probabilistic neural output against strict symbolic rules.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.symbolic_rules: List[Dict[str, Any]] = [
            {"name": "No deletions", "regex": r"delete|rm -rf", "impact": "BLOCK"},
            {"name": "Type Safety", "regex": r":\s*(int|str|List|Dict|Any)", "impact": "PREFER"},
            {"name": "No plain passwords", "regex": r'password\s*=\s*[\'"][^\'"]+[\'"]', "impact": "BLOCK"}
        ]
        self._system_prompt = (
            "You are the Neuro-Symbolic Agent. "
            "Your job is to take raw AI suggestions and validate them against formal symbolic constraints. "
            "You prevent logical violations and ensure structural integrity."
        )

    @as_tool
    def verify_and_correct(self, content: str) -> Dict[str, Any]:
        """
        Validates content against symbolic rules and attempts to flag violations.
        """
        logging.info("NeuroSymbolic: Validating content against symbolic rules.")
        violations = []
        
        for rule in self.symbolic_rules:
            if re.search(rule["regex"], content, re.IGNORECASE):
                violations.append({
                    "rule": rule["name"],
                    "impact": rule["impact"],
                    "action": "CORRECTION_REQUIRED" if rule["impact"] == "BLOCK" else "ADVISORY"
                })
        
        passed = all(v["impact"] != "BLOCK" for v in violations)
        
        return {
            "content_verified": passed,
            "violations": violations,
            "corrected_content": content if passed else "# BLOCK: Symbolic Rule Violation Detected"
        }

    def improve_content(self, prompt: str) -> str:
        res = self.verify_and_correct(prompt)
        return res["corrected_content"]