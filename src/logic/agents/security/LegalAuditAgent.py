import re
import json
import logging
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.version import VERSION

__version__ = VERSION

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
