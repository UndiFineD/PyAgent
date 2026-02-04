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

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class RedTeamChallenge:
    id: int
    title: str
    category: str
    goal: str
    metaprompt: str
    scoring_regex: Optional[str] = None
    success_message: str = "Challenge Completed"

class RedTeamCore:
    """
    Manages security 'Challenges' and internal red-teaming scenarios.
    Used to stress-test GuardrailCore and identify prompt injection vulnerabilities.
    Harvested from .external/AI-Red-Teaming-Playground-Labs pattern.
    """

    def __init__(self, challenges_path: str = ".external/AI-Red-Teaming-Playground-Labs/challenges/challenges.json"):
        self.challenges: List[RedTeamChallenge] = []
        self._load_challenges(challenges_path)

    def _load_challenges(self, path: str):
        p = Path(path)
        if not p.exists():
            return

        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                for c in data.get("Challenges", []):
                    scorer = c.get("Scorer", {})
                    self.challenges.append(RedTeamChallenge(
                        id=c["challenge_id"],
                        title=c["challenge_title"],
                        category=c["category"],
                        goal=c["goal"],
                        metaprompt=c["metaprompt"],
                        scoring_regex=scorer.get("instruction") if scorer.get("isRegex") else None,
                        success_message=scorer.get("message", "Success")
                    ))
        except Exception as e:
            print(f"Error loading challenges: {e}")

    def evaluate_response(self, challenge_id: int, response_text: str) -> bool:
        """Checks if a response successfully completes a challenge."""
        challenge = next((c for c in self.challenges if c.id == challenge_id), None)
        if not challenge or not challenge.scoring_regex:
            return False
        
        return bool(re.search(challenge.scoring_regex, response_text, re.IGNORECASE))

    def get_metaprompt(self, challenge_id: int) -> Optional[str]:
        """Returns the metaprompt for a specific challenge."""
        challenge = next((c for c in self.challenges if c.id == challenge_id), None)
        return challenge.metaprompt if challenge else None
