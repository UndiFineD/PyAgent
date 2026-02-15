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
Compliance agent.py module.
"""

import logging
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

# Ensure relative or absolute import matches structure
try:
    from src.logic.agents.compliance.core.compliance_core import ComplianceCore
except ImportError:
    # If core doesn't exist yet, we might need to mock or it is in a different place
    pass

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ComplianceAgent(BaseAgent):
    """Shell agent for continuous compliance and regulatory auditing.
    Coordinates fleet-wide scans and reports violations to the security layer.
    """

    def __init__(self, file_path: str | None = None) -> None:
        super().__init__(file_path if file_path else "virtual_compliance_agent")
        try:
            self.core = ComplianceCore()
        except NameError:
            self.core = None  # Handle missing core gracefully
        self.history: list[dict[str, Any]] = []

    def scan_shard(self, content: str) -> dict:
        """Scans a memory shard for compliance issues (Phase 57)."""
        import re

        patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        }
        findings = []
        for name, pattern in patterns.items():
            if re.search(pattern, content):
                findings.append(name)
        return {"compliant": len(findings) == 0, "findings": findings, "pii_detected": len(findings) > 0}

    @as_tool
    def perform_audit(self, file_map: dict[str, str]) -> dict[str, Any]:
        """Audits a map of file_paths to content."""
        if not self.core:
            return {"status": "ERROR", "message": "ComplianceCore missing"}

        all_issues = []
        for path, content in file_map.items():
            issues = self.core.audit_content(content, path)
            all_issues.extend(issues)

        score = self.core.aggregate_score(all_issues)

        report = {
            "score": score,
            "issue_count": len(all_issues),
            "critical_violations": [i.message for i in all_issues if i.severity == "CRITICAL"],
            "status": "PASS" if score > 0.8 else "FAIL",
        }

        self.history.append(report)
        logging.info(f"Compliance Report: Score {score:.2f} ({report['status']})")

        return report
