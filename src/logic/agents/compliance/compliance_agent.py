from src.core.base.version import VERSION
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import as_tool
import logging
from typing import Any

# Ensure relative or absolute import matches structure
try:
    from src.logic.agents.compliance.core.compliance_core import (
        ComplianceCore,
    )
except ImportError:
    # If core doesn't exist yet, we might need to mock or it is in a different place
    pass

__version__ = VERSION


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
        return {
            "compliant": len(findings) == 0,
            "findings": findings,
            "pii_detected": len(findings) > 0
        }

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
            "critical_violations": [
                i.message for i in all_issues if i.severity == "CRITICAL"
            ],
            "status": "PASS" if score > 0.8 else "FAIL",
        }

        self.history.append(report)
        logging.info(f"Compliance Report: Score {score:.2f} ({report['status']})")

        return report
