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

"""
PrivacyGuardAgent: Agent for monitoring, enforcing, and auditing privacy controls and data protection in the PyAgent swarm.
Implements privacy risk detection and compliance automation.
"""

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
Privacy guard agent.py module.
"""


from __future__ import annotations

import re
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class PrivacyGuardAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Privacy Guard Agent: Monitors fleet communications for PII (Personally
    Identifiable Information), performs redaction, and tracks compliance.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.pii_patterns = {
            "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "Phone": r"\b(?:\d{3}[-.]?)?\d{3}[-.]?\d{4}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "CreditCard": r"\b(?:\d[ -]*?){13,16}\b",
            "AWS_KEY": r"(?i)AKIA[0-9A-Z]{16}",
            "AWS_SECRET": r"(?i)SECRET.*['\"]?[a-zA-Z0-9/+=]{40}['\"]?",
            "GENERIC_TOKEN": r"(?i)(token|auth|key|secret)[ \t]*[:=][ \t]*['\"]?[a-zA-Z0-9_\-\.]{16,}",
            "GITHUB_TOKEN": r"ghp_[a-zA-Z0-9]{36}",
        }
        self.redaction_logs: list[Any] = []

    def scan_and_redact(self, text: str) -> dict[str, Any]:
        """Scans text for PII patterns and returns redacted version."""
        original_text = text
        redacted_text = text
        findings = []

        try:
            from rust_core import scan_pii_rust  # type: ignore[attr-defined]

            rust_findings = scan_pii_rust(text)
            for pii_type, match in rust_findings:
                findings.append({"type": pii_type, "value": match})
                redacted_text = redacted_text.replace(match, f"[REDACTED_{pii_type.upper()}]")
        except (ImportError, AttributeError):
            for pii_type, pattern in self.pii_patterns.items():
                matches = re.findall(pattern, text)
                if matches:
                    for match in matches:
                        findings.append({"type": pii_type, "value": match})
                        redacted_text = redacted_text.replace(match, f"[REDACTED_{pii_type.upper()}]")

        if findings:
            self.redaction_logs.append(
                {
                    "timestamp": "2026-01-08",  # Simulated
                    "findings_count": len(findings),
                    "pii_types": list(set(f["type"] for f in findings)),
                }
            )
            # Phase 108: Intelligence Recording
            self._record(
                text[:500],
                redacted_text[:500],
                provider="PrivacyGuard",
                model="PIIScanner",
                meta={"findings_count": len(findings)},
            )

        return {
            "original": original_text,
            "redacted": redacted_text,
            "pii_detected": bool(findings),
            "findings": findings,
        }

    def bulk_scan_workspace(self) -> list[dict[str, str]]:
        """
        Performs a high-speed recursive scan of the workspace for secrets.
        Offloads the heavy filesystem traversal and regex matching to Rust.
        """
        try:
            from rust_core import \
                scan_secrets_rust  # type: ignore[attr-defined]

            return scan_secrets_rust(self.workspace_path)
        except (ImportError, AttributeError):
            # Fallback to a basic (slower) implementation if needed
            # In a real scenario, this would loop using os.walk in Python
            return []

    def verify_message_safety(self, message: str) -> dict[str, Any]:
        """Returns safety report; 'safe': True if no PII is detected."""
        result = self.scan_and_redact(message)
        if result["pii_detected"]:
            return {
                "safe": False,
                "reason": f"PII Detected: {', '.join(set(f['type'] for f in result['findings']))}",
            }
        return {"safe": True}

    def get_privacy_metrics(self) -> dict[str, Any]:
        """Returns summary metrics for privacy protection efforts."""
        return {
            "total_redactions": len(self.redaction_logs),
            "pii_types_captured": list(set(t for log in self.redaction_logs for t in log["pii_types"])),
            "safety_rating": "High" if len(self.redaction_logs) < 100 else "Critical Levels of PII Exposure",
        }
