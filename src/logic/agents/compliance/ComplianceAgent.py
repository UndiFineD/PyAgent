from src.core.base.Version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool
import logging
from typing import Any

# Ensure relative or absolute import matches structure
try:
    from src.logic.agents.compliance.core.ComplianceCore import (
        ComplianceCore,
        ComplianceIssue,
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

    @as_tool
    def perform_audit(self, file_map: dict[str, str]) -> dict[str, Any]:
        """Audits a map of file_paths to content."""
        if not self.core:
            return {"status": "ERROR", "message": "ComplianceCore missing"}

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
