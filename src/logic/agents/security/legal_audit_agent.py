#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

"""
LegalAuditAgent - Legal compliance and smart contract auditing

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with repository path: agent = LegalAuditAgent("path/to/project")
- Scan source text for licenses: agent.scan_licensing(file_contents)
- Enforce project policy: agent.check_license_compliance(file_contents, project_license="MIT")
- Audit smart contracts: agent.verify_smart_contract(solidity_source)
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
    """Structured report for license auditing."""

    detected_licenses: list[str]
    risk_level: str
    summary: str
    is_compliant: bool
    violations: list[str]
    action_required: str
    risk_summary: str


class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 59: Autonomous Legal & Smart Contract Auditing.
    Scans codebases for licensing risks, liability concerns, and smart contract vulnerabilities.
    """

    def __init__(self, path: str, **kwargs: Any) -> None:
        super().__init__(path, **kwargs)
        self.license_patterns = {
            "GPL": r"GPL|General Public License",
            "AGPL": r"AGPL|Affero General Public License",
            "MIT": r"MIT License",
            "Apache": r"Apache License 2\.0",
        }
        self.license_blacklist = [
            "GPL",
            "AGPL",
        ]  # Blacklist for non-copyleft projects (Phase 238)

    def _record(self, prompt: str, result: str, provider: str = "LegalAudit", model: str = "v1") -> None:
        """Internal helper to record interactions to the swarm context."""
        if hasattr(self, "recorder") and self.recorder:
            try:
                self.recorder.record_interaction(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    result=result,
                    meta={"timestamp": time.time(), "agent": "LegalAuditAgent"},
                )
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    def check_license_compliance(self, content: str, project_license: str = "MIT") -> LicenseReport:
        """
        Phase 238: Check generated code against a license blacklist to prevent
        GPL/AGPL contamination in permissive projects.
        """
        _ = project_license
        scan = self.scan_licensing(content)
        violations = [
            license_name for license_name in scan.get("detected_licenses", []) if license_name in self.license_blacklist
        ]

        is_compliant = not violations
        res: LicenseReport = {
            "is_compliant": is_compliant,
            "detected_licenses": scan.get("detected_licenses", []),
            "violations": violations,
            "action_required": "Block / Rewrite" if not is_compliant else "None",
            "risk_level": scan.get("risk_level", "low"),
        }
        return res

    def scan_licensing(self, content: str) -> LicenseReport:
        """Identifies licenses and flags copyleft risks."""
        detected = []
        for name, pattern in self.license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        res: LicenseReport = {
            "detected_licenses": detected,
            "risk_level": "high" if any(license_name in ["GPL", "AGPL"] for license_name in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}",
        }
        # Phase 108: Intelligence Recording
        self._record(content[:1000], str(res), provider="LegalAudit", model="LicenseScanner")
        return res

    def verify_smart_contract(self, logic: str) -> dict[str, Any]:
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
            "threat_score": len(vulnerabilities) * 2.5,
        }

    def generate_liability_report(self, task_output: str) -> str:
        """Analy
"""

from __future__ import annotations

import re
import time
from typing import Any, TypedDict

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LicenseReport(TypedDict, total=False):
    """Structured report for license auditing."""

    detected_licenses: list[str]
    risk_level: str
    summary: str
    is_compliant: bool
    violations: list[str]
    action_required: str
    risk_summary: str


class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 59: Autonomous Legal & Smart Contract Auditing.
    Scans codebases for licensing risks, liability concerns, and smart contract vulnerabilities.
    """

    def __init__(self, path: str, **kwargs: Any) -> None:
        super().__init__(path, **kwargs)
        self.license_patterns = {
            "GPL": r"GPL|General Public License",
            "AGPL": r"AGPL|Affero General Public License",
            "MIT": r"MIT License",
            "Apache": r"Apache License 2\.0",
        }
        self.license_blacklist = [
            "GPL",
            "AGPL",
        ]  # Blacklist for non-copyleft projects (Phase 238)

    def _record(self, prompt: str, result: str, provider: str = "LegalAudit", model: str = "v1") -> None:
        """Internal helper to record interactions to the swarm context."""
        if hasattr(self, "recorder") and self.recorder:
            try:
                self.recorder.record_interaction(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    result=result,
                    meta={"timestamp": time.time(), "agent": "LegalAuditAgent"},
                )
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    def check_license_compliance(self, content: str, project_license: str = "MIT") -> LicenseReport:
        """
        Phase 238: Check generated code against a license blacklist to prevent
        GPL/AGPL contamination in permissive projects.
        """
        _ = project_license
        scan = self.scan_licensing(content)
        violations = [
            license_name for license_name in scan.get("detected_licenses", []) if license_name in self.license_blacklist
        ]

        is_compliant = not violations
        res: LicenseReport = {
            "is_compliant": is_compliant,
            "detected_licenses": scan.get("detected_licenses", []),
            "violations": violations,
            "action_required": "Block / Rewrite" if not is_compliant else "None",
            "risk_level": scan.get("risk_level", "low"),
        }
        return res

    def scan_licensing(self, content: str) -> LicenseReport:
        """Identifies licenses and flags copyleft risks."""
        detected = []
        for name, pattern in self.license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        res: LicenseReport = {
            "detected_licenses": detected,
            "risk_level": "high" if any(license_name in ["GPL", "AGPL"] for license_name in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}",
        }
        # Phase 108: Intelligence Recording
        self._record(content[:1000], str(res), provider="LegalAudit", model="LicenseScanner")
        return res

    def verify_smart_contract(self, logic: str) -> dict[str, Any]:
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
            "threat_score": len(vulnerabilities) * 2.5,
        }

    def generate_liability_report(self, task_output: str) -> str:
        """Analyzes agent output for language that might imply legal liability."""
        liability_keywords = ["guarantee", "perfect", "100% safe", "no risk"]
        flags = [w for w in liability_keywords if w in task_output.lower()]

        if flags:
            return (
                f"WARNING: Potential liability flags detected in output: {', '.join(flags)}. "
                "Recommend adding disclaimers."
            )
        return "No significant liability language detected."
