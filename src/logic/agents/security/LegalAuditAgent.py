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



import re
import json
import logging
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent


class LegalAuditAgent(BaseAgent):
    """
    Phase 59: Autonomous Legal & Smart Contract Auditing.
    Scans codebases for licensing risks, liability concerns, and smart contract vulnerabilities.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.license_patterns = {
            "GPL": r"GPL|General Public License",
            "AGPL": r"AGPL|Affero General Public License",
            "MIT": r"MIT License",
            "Apache": r"Apache License 2\.0"
        }
        self.license_blacklist = ["GPL", "AGPL"] # Blacklist for non-copyleft projects (Phase 238)

    def check_license_compliance(self, content: str, project_license: str = "MIT") -> Dict[str, Any]:
        """
        Phase 238: Check generated code against a license blacklist to prevent 
        GPL/AGPL contamination in permissive projects.
        """
        scan = self.scan_licensing(content)
        violations = [l for l in scan["detected_licenses"] if l in self.license_blacklist]
        
        is_compliant = len(violations) == 0
        return {
            "is_compliant": is_compliant,
            "detected_licenses": scan["detected_licenses"],
            "violations": violations,
            "action_required": "Block / Rewrite" if not is_compliant else "None"
        }

    def scan_licensing(self, content: str) -> Dict[str, Any]:
        """Identifies licenses and flags copyleft risks."""
        detected = []
        for name, pattern in self.license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)
        
        res = {
            "detected_licenses": detected,
            "risk_level": "high" if any(l in ["GPL", "AGPL"] for l in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}"
        }
        # Phase 108: Intelligence Recording
        self._record(content[:1000], str(res), provider="LegalAudit", model="LicenseScanner")
        return res

    def verify_smart_contract(self, logic: str) -> Dict[str, Any]:
        """Simulates auditing a smart contract for common vulnerabilities."""
        vulnerabilities = []
        if "reentrancy" in logic.lower() or ".call{value:" in logic:
            vulnerabilities.append("Potential Reentrancy Vulnerability")
        if "tx.origin" in logic:
            vulnerabilities.append("Insecure use of tx.origin")
        if "selfdestruct" in logic:
            vulnerabilities.append("Critical: selfdestruct found")
            
        return {
            "status": "fail" if vulnerabilities else "pass",
            "vulnerabilities": vulnerabilities,
            "threat_score": len(vulnerabilities) * 2.5
        }

    def generate_liability_report(self, task_output: str) -> str:
        """Analyzes agent output for language that might imply legal liability."""
        liability_keywords = ["guarantee", "perfect", "100% safe", "no risk"]
        flags = [w for w in liability_keywords if w in task_output.lower()]
        
        if flags:
            return f"WARNING: Potential liability flags detected in output: {', '.join(flags)}. Recommend adding disclaimers."
        return "No significant liability language detected."
