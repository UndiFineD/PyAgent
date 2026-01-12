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


"""Persistent audit log for safety violations and adversarial attempts."""




import json
import logging
from pathlib import Path
from datetime import datetime

class SafetyAuditTrail:
    """Logs security violations for later forensic analysis and training."""
    
    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.violations = []
        self._load_log()

    def _load_log(self) -> str:
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    self.violations = json.load(f)
            except Exception as e:
                logging.error(f"SafetyAuditTrail: Error loading log: {e}")

    def log_violation(self, agent_name: str, task: str, violations: list, level: str = "HIGH") -> str:
        """Records a new safety violation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "level": level,
            "violations": violations,
            "context": task[:500]
        }
        self.violations.append(entry)
        self._save_log()
        logging.warning(f"SafetyAuditTrail: Logged {level} violation for {agent_name}.")

    def _save_log(self) -> str:
        try:
            with open(self.log_path, 'w') as f:
                json.dump(self.violations, f, indent=2)
        except Exception as e:
            logging.error(f"SafetyAuditTrail: Error saving log: {e}")

    def get_summary(self) -> str:
        """Returns a human-readable summary of recently logged threats."""
        if not self.violations:
            return "No safety violations recorded."
        return f"Safety Audit: {len(self.violations)} threats recorded. Latest: {self.violations[-1]['level']} at {self.violations[-1]['timestamp']}"
