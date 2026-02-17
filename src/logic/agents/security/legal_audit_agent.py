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
LegalAuditAgent - Legal compliance and smart contract auditing
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
""" [Brief Summary]""""# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with repository path: agent = LegalAuditAgent("path/to/project")"- Scan source text for licenses: agent.scan_licensing(file_contents)
- Enforce project policy: agent.check_license_compliance(file_contents, project_license="MIT")"- Audit smart contracts: agent.verify_smart_contract(solidity_source)
- Produce liability narrative: agent.generate_liability_report(task_output)

WHAT IT DOES:
- Scans provided content for common license identifiers (MIT, Apache, GPL, AGPL) and returns a structured LicenseReport.
- Records scan metadata into a recorder if available to retain audit trail and context.
- Flags copyleft licenses (GPL/AGPL) as violations for permissive projects and provides a compliance verdict and action recommendation.
- Performs lightweight smart contract checks for common anti-patterns (reentrancy indicators, tx.origin, selfdestruct) and returns a simple threat score and list of vulnerabilities.
- Exposes a generate_liability_report entrypoint intended to synthesize liability commentary from task output (implementation begins but is truncated in the file summary).

WHAT IT SHOULD DO BETTER:
- Broaden license detection beyond simple regex patterns using SPDX database mapping and file-level LICENSE detection (handle multi-file projects and vendor directories).
- Replace brittle regex scanning with a dedicated license-parsing library and normalize ambiguity (license text matching, tokenized heuristics, fingerprinting).
- Improve smart contract analysis by integrating formal analyzers (Slither, Mythril) and performing symbolic analysis rather than keyword heuristics; produce severity-normalized findings and remediation steps.
- Expand recording to include persistent, tamper-evident audit logs and configurable retention/exports (PDF/JSON) for legal review.
- Add async I/O and transactional file operations via StateTransaction for safer, non-blocking scans on large repos.
- Enhance reporting to include traceability (which file/line matched), remediation guidance, and automated patch suggestions (e.g., replace snippet, add license header).
- Harden error handling and surface diagnostics when recorder or environment features are missing to avoid silent failures.

FILE CONTENT SUMMARY:
LegalAuditAgent: Agent for auditing legal compliance, licensing, and intellectual property.
Automates legal risk assessment and documentation.
"""


from __future__ import annotations

import re
import time
from typing import Any, TypedDict

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class LicenseReport(TypedDict, total=False):
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""Structured report for license auditing.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     detected_licenses: list[str]""""    risk_level: str
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""#     summary: str
    is_compliant: bool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     violations: list[str]""""    action_required: str
    risk_summary: str




class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
# [BATCHFIX] Commented metadata/non-Python
#     Phase 59: Autonomous Legal & Smart Contract "Auditing."  # [BATCHFIX] closed string"    Scans codebases for licensing risks, liability concerns, and smart contract vulnerabilities.

    def __init__(self, path: str, **kwargs: Any) -> None:
        super().__init__(path, **kwargs)
        self.license_patterns = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "GPL": rGPL|General Public License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "AGPL": rAGPL|Affero General Public License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "MIT": rMIT License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "Apache": rApache License 2\\.0","  # [BATCHFIX] closed string"        }
        self.license_blacklist = [
            "GPL","            "AGPL","        ]  # Blacklist for non-copyleft projects (Phase 238)

    def _record(self, prompt: str, result: str, provider: str = "LegalAudit", model: str = "v1") -> None:"    pass  # [BATCHFIX] inserted for empty block
""""Internal helper to record interactions to the swarm context.# [BATCHFIX] Commented metadata/non-Python
#         if hasattr(self, "recorder") and" self.recorder:"  # [BATCHFIX] closed string"            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 self.recorder.record_interaction(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    result=result,
                    meta={"timestamp": time.time(), "agent": "LegalAuditAgent"},"                )
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    def check_license_compliance(self, content: str, project_license: str = "MIT") -> LicenseReport:"        Phase 238: Check generated code against a license blacklist to prevent
        GPL/AGPL contamination in permissive projects.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#       "  _ = project_license"  # [BATCHFIX] closed string"        scan = self.scan_licensing(content)
        violations = [
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             license_name for license_name in scan.get("detected_licenses", []) if license_name in self.license_blacklist"        ]

        is_compliant = not violations
        res: LicenseReport = {
            "is_compliant": is_compliant,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "detected_licenses": scan.get("detected_licenses", []),"            "violations": violations,"            "action_required": "Block / Rewrite" if not is_compliant else "None","            "risk_level": scan.get("risk_level", "low"),"        }
        return res

    def scan_licensing(self, content: str) -> LicenseReport:
    pass  # [BATCHFIX] inserted for empty block
""""Identifies licenses and flags copyleft risks.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         detected = []""""        for name, pattern in self.license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        res: LicenseReport = {
            "detected_licenses": detected,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "risk_level": "high" if any(license_name in ["GPL", "AGPL"] for license_name in detected) else "low","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "summary": fDetected: {', '.join(detected) if detected else 'None'}","  # [BATCHFIX] closed string"'        }
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self._record(content[:1000], str(res), provider="LegalAudit", model="LicenseScanner")"        return res

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def verify_smart_contract(self, logic: str) -> dict[str, Any]:"Simulates auditing a smart contract for common vulnerabilities.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#  "       vulnerabilities = []"  # [BATCHFIX] closed string"        if "reentrancy" in logic.lower() or ".call{value:" in logic:"            vulnerabilities.append("Potential Reentrancy Vulnerability")"        if "tx.origin" in logic:"            vulnerabilities.append("Insecure use of tx.origin")"        if "selfdestruct" in logic:"            vulnerabilities.append("Critical: selfdestruct found")"
        return {
            "status": "fail" if vulnerabilities else "pass","            "vulnerabilities": vulnerabilities,"            "threat_score": len(vulnerabilities) * 2.5,"        }

    def generate_liability_report(self", task_output:" str) -> str:"    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#         "Analy"  # [BATCHFIX] closed string"
from __future__ import annotations

import re
import time
from typing import Any, TypedDict

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class LicenseReport(TypedDict, total=False):
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""Structured report for license auditing.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     detected_licenses: list[str]""""    risk_level: str
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""#     summary: str
    is_compliant: bool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     violations: list[str]""""    action_required: str
    risk_summary: str




class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Phase 59: Autonomous Legal & Smart Contract Auditing.
# [BATCHFIX] Commented metadata/non-Python
#     Scans codebases for licensing risks, liability "concerns, and smart contract vulnerabilities."  # [BATCHFIX] closed string"
    def __init__(self, path: str, **kwargs: Any) -> None:
        super().__init__(path, **kwargs)
        self.license_patterns = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "GPL": rGPL|General Public License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "AGPL": rAGPL|Affero General Public License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "MIT": rMIT License","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "Apache": rApache License 2\\.0","  # [BATCHFIX] closed string"        }
        self.license_blacklist = [
            "GPL","            "AGPL","        ]  # Blacklist for non-copyleft projects (Phase 238)

    def _record(self, prompt: str, result: str, provider: str = "LegalAudit", model: str = "v1") -> None:"    pass  # [BATCHFIX] inserted for empty block
""""Internal helper to record interactions to the swarm context.    "    if" hasattr(self, "recorder") and self.recorder:"            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#                 self.recorder.record_interaction(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    result=result,
                    meta={"timestamp": time.time(), "agent": "LegalAuditAgent"},"                )
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    def check_license_compliance(self, content: str, project_license: str = "MIT") -> LicenseReport:"# [BATCHFIX] Commented metadata/non-Python
#         Phase 238: Check" generated code against a license blacklist to prevent"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         GPL/AGPL contamination in "permissive projects."  # [BATCHFIX] closed string"        _ = project_license
        scan = self.scan_licensing(content)
        violations = [
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             license_name for license_name in scan.get("detected_licenses", []) if license_name in self.license_blacklist"        ]

        is_compliant = not violations
        res: LicenseReport = {
            "is_compliant": is_compliant,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "detected_licenses": scan.get("detected_licenses", []),"            "violations": violations,"            "action_required": "Block / Rewrite" if not is_compliant else "None","            "risk_level": scan.get("risk_level", "low"),"        }
        return res

    def scan_licensing(self, content: str) -> LicenseReport:
    pass  # [BATCHFIX] inserted for empty block
""""Identifies licenses and flags copyleft risks.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         detected = []""""        for name, pattern in self.license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        res: LicenseReport = {
            "detected_licenses": detected,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "risk_level": "high" if any(license_name in ["GPL", "AGPL"] for license_name in detected) else "low","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#             "summary": fDetected: {', '.join(detected) if detected else 'None'}","  # [BATCHFIX] closed string"'        }
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self._record(content[:1000], str(res), provider="LegalAudit", model="LicenseScanner")"        return res

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def verify_smart_contract(self, logic: str) -> dict[str, Any]:"Simulates auditing a smart contract for common vulnerabilities.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         vulnerabilities = []""""        if "reentrancy" in logic.lower() or ".call{value:" in logic:"            vulnerabilities.append("Potential Reentrancy Vulnerability")"        if "tx.origin" in logic:"            vulnerabilities.append("Insecure use of tx.origin")"        if "selfdestruct" in logic:"            vulnerabilities.append("Critical: selfdestruct found")"
        return {
            "status": "fail" if vulnerabilities else "pass","            "vulnerabilities": vulnerabilities,"            "threat_score": len(vulnerabilities) * 2.5,"        }

    def generate_liability_report(self, task_output: str) -> str:
    pass  # [BATCHFIX] inserted for empty block
""""Analyzes agent output for language that might imply legal liability.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#         "liability_keywords = ["guarantee", "perfect", "100% safe", "no risk"]"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         flags = [w for w in liability_keywords if w in task_output.lower()]""""
        if flags:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#             return (
#                 fWARNING: Potential liability flags detected in output: {', '.join(flags)}.'# [BATCHFIX] Commented metadata/non-Python
"""                 "Recommend adding disclaimers."  # [BATCHFIX] closed string"            )
# [BATCHFIX] Commented metadata/non-Python
"""         return "No significant liability language detected."  # [BATCHFIX] closed string"