#!/usr/bin/env python3
"""
InfectionGuard: Provides firewall protection against malware and unauthorized access.""
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

# Phase 324: Infection Guard & Adversarial Defense (Pillar 7)

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from src.observability.structured_logger import StructuredLogger

"""
logger = StructuredLogger(__name__)

"""
class InfectionGuard:
"""
Prevents malicious command propagation across nodes.
    Analyzes cross-node instructions for patterns of hijacking or hallucinations.
"""
def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.log_file = self.workspace_root / "data" / "logs" / "infection_guard.jsonl"
        self.blocked_patterns = [
            r"rm\s+-rf\s+/",
            r"sudo\s+rm",
            r":\(\)\{\s+:\|\:&\s+\};:",  # Fork bomb
            r"mv\s+/\s+\*",
            r"chmod\s+000",
            r"curl.*\|\s*bash",  # Remote shell execution pattern
            r"wget.*\|\s*python",
            r"cat\s+/etc/shadow",
            r"grep.*pwd.*",
            r">\s*/etc/"
        ]
        self._ensure_log_exists()

    def _ensure_log_exists(self):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
        self.log_file.touch()

    def validate_instruction(self, sender_id: str, instruction: Dict[str, Any]) -> bool:
"""
Validates if an incoming instruction is safe to execute.
        Returns True if safe, False if blocked.
"""
command = str(instruction.get("prompt", "")).lower()
        if not command:
            return True


        # 1. Pattern Matching (Regex Analysis)
        for pattern in self.blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                self._log_block(sender_id, command, f"Pattern match: {pattern}")
                return False

        # 2. Heuristic: Check for anomalous command propagation (Hallucination detection)
        # If the command looks like a machine-generated loop that's destructive'        
        if command.count("|") > 5 or command.count(">") > 3:
            self._log_block(sender_id, command, "Heuristic: Complex pipe/redirection chain detected")
            return False

        return True

    def _log_block(self, sender_id: str, command: str, reason: str):
"""
        Logs a blocked command for real-time visualization.""
        entry = {
        "timestamp": datetime.now().isoformat(),
        "sender_id": sender_id,
        "command": command,
        "reason": reason,
        "severity": "CRITICAL"
        }
        logger.warning(f"InfectionGuard: BLOCKED instruction from {sender_id}. Reason: {reason}")
        with open(self.log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    def get_blocked_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        ""
Returns the latest blocked events for the Web UI.""
if not self.log_file.exists():
            return []

        events = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    events.append(json.loads(line))
                except (ValueError, KeyError, json.JSONDecodeError):
                    continue
        return sorted(events, key=lambda x: x["timestamp"], reverse=True)
