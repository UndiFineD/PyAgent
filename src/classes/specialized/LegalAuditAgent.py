import re
import json
import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent

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
        
        return {
            "detected_licenses": detected,
            "risk_level": "high" if any(l in ["GPL", "AGPL"] for l in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}"
        }

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
