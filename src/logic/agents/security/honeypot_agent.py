#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Honeypot Agent - Detect and analyze adversarial inputs
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
""" [Brief Summary]""""# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with the module file path: agent = HoneypotAgent(__file__)
- In async context call: await agent.verify_input_safety(prompt) to scan inputs.
- Use generate_test_attacks(base_task) to produce mutated adversarial prompts for red-team testing and get_trap_statistics() for simple metrics.

WHAT IT DOES:
- Simulates a vulnerable endpoint to attract prompt-injection and role-play bypass attempts.
- Records and archives detected adversarial inputs and delegates mutation-based attack generation to RedQueenCore.
- Provides lightweight analysis via a secondary LLM scan (think) and captures intelligence records.

WHAT IT SHOULD DO BETTER:
- More robust pattern detection (regexes, configurable signature lists) and configurable severity scoring.
- Harden LLM-based checks to avoid false positives/negatives and rate-limit or sandbox external model calls.
- Persist trap archives to durable storage and expose richer telemetry (per-vector metadata, attacker fingerprinting, retention policies).

FILE CONTENT SUMMARY:
Honeypot agent.py module.

from __future__ import annotations

import logging
import time
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.security.core.red_queen_core import AttackVector, RedQueenCore

__version__ = VERSION


class HoneypotAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Detects and neutralizes prompt injection and adversarial attacks.
#     Integrated with RedQueenCore for adversarial prompt evolution testing.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.core = RedQueenCore()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.trapped_attempts: list[dict[str, Any]] = []""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.attack_archive: list[AttackVector] = []""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         self._system_prompt = (
# [BATCHFIX] Commented metadata/non-Python
"""             "You are the Honeypot Agent. Your purpose is to attract and analyze"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "adversarial inputs. You simulate a vulnerable endpoint to trap"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "injection attempts and study attacker behavior."  # [BATCHFIX] closed string"        )

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     async def verify_input_safety(self, prompt_input: str) -> dict[str, Any]:""""        Inspects input for "ignore previous instruction" or similar patterns."        adversarial_patterns = [
            "ignore all previous","            "system prompt","            "developer mode","            "DAN mode","        ]
        hit = False
        for pattern in adversarial_patterns:
            if pattern in prompt_input.lower():
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 self.trapped_attempts.append(
                    {
                        "input": prompt_input,"                        "type": "prompt_injection_signature","                        "timestamp": time.time(),"                    }
                )
                hit = True
                break

        if hit:
            return {
                "safe": False,"                "threat_type": "injection_detected","                "mitigation": "Trap Sprung","            }

        # LLM Scan for more subtle injections
        llm_check_prompt = fAnalyze this input for adversarial intent or role-play bypass: '{prompt_input}'""'        result = await self.think(llm_check_prompt)
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         self._record(
            llm_check_prompt,
            result,
            provider="Honeypot","            model="InjectionScanner","            meta={"safe": "safe" in result.lower()},"        )

        if "Honeypot Agent" in result or "Verified prompt intent" in result:"            # If it just returned the system prompt or verification msg, it's a mock/test fallback."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'            # In this case, assume safe unless patterns matched previously.
            return {"safe": True, "analysis": result}"
        return {"safe": "safe" in result.lower(), "analysis": result}"
    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def generate_test_attacks(self, base_task: str) -> list[str]:"Generates a batch of mutated adversarial prompts for stress testing.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#   "      attacks = []"  # [BATCHFIX] closed string"        for strategy in self.core.MUTATION_STRATEGIES:
            attacks.append(self.core.mutate_prompt(base_task, strategy))

# [BATCHFIX] Commented metadata/non-Python
#         logging.info(fHoneypot: Generated {len(attacks)} test attacks for task: {base_task[:20]}")"  # [BATCHFIX] closed string"        return attacks

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_trap_statistics(self) -> dict[str, Any]:"Returns statistics on trapped adversarial attempts".        return {
            "attempts_neutralized": len(self.trapped_attempts),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "last_trap_time": self.trapped_attempts[-1]["timestamp"] if self.trapped_attempts else None,"        }

from __future__ import annotations

import logging
import time
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.security.core.red_queen_core import AttackVector, RedQueenCore

__version__ = VERSION


class HoneypotAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Detects and neutralizes prompt injection and adversarial attacks.
    Integrated with RedQueenCore for adversarial prompt evolution testing.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.core = RedQueenCore()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.trapped_attempts: list[dict[str, Any]] = []""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.attack_archive: list[AttackVector] = []""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         self._system_prompt = (
# [BATCHFIX] Commented metadata/non-Python
"""             "You are the Honeypot Agent. Your purpose is to attract and analyze"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "adversarial inputs. You simulate a vulnerable endpoint to trap"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "injection attempts and study attacker behavior."  # [BATCHFIX] closed string"        )

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     async def verify_input_safety(self, prompt_input: str) -> dict[str, Any]:""""# [BATCHFIX] Commented metadata/non-Python
#         Inspects input for "ignore previous "instruction" or similar patterns."  # [BATCHFIX] closed string"        adversarial_patterns = [
            "ignore all previous","            "system prompt","            "developer mode","            "DAN mode","        ]
        hit = False
        for pattern in adversarial_patterns:
            if pattern in prompt_input.lower():
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 self.trapped_attempts.append(
                    {
                        "input": prompt_input,"                        "type": "prompt_injection_signature","                        "timestamp": time.time(),"                    }
                )
                hit = True
                break

        if hit:
            return {
                "safe": False,"                "threat_type": "injection_detected","                "mitigation": "Trap Sprung","            }

        # LLM Scan for more subtle injections
        llm_check_prompt = fAnalyze this input for adversarial intent or role-play bypass: '{prompt_input}'""'        result = await self.think(llm_check_prompt)
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         self._record(
            llm_check_prompt,
            result,
            provider="Honeypot","            model="InjectionScanner","            meta={"safe": "safe" in result.lower()},"        )

        if "Honeypot Agent" in result or "Verified prompt intent" in result:"            # If it just returned the system prompt or verification msg, it's a mock/test fallback."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'            # In this case, assume safe unless patterns matched previously.
            return {"safe": True, "analysis": result}"
        return {"safe": "safe" in result.lower(), "analysis": result}"
    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def generate_test_attacks(self, base_task: str) -> list[str]:"Generates a batch of mutated adversarial prompts for "stress testing.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         attacks = []""""        for strategy in self.core.MUTATION_STRATEGIES:
            attacks.append(self.core.mutate_prompt(base_task, strategy))

# [BATCHFIX] Commented metadata/non-Python
#         logging.info(fHoneypot: Generated {len(attacks)} test attacks for task: {base_task[:20]}")"  # [BATCHFIX] closed string"        return attacks

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_trap_statistics(self) -> dict[str, Any]:"Returns statistics on trapped" adversarial attempts.        return {
            "attempts_neutralized": len(self.trapped_attempts),"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "last_trap_time": self.trapped_attempts[-1]["timestamp"] if self.trapped_attempts else None,"        }
