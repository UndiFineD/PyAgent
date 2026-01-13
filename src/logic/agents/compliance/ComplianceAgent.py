
from src.core.base.version import VERSION
import logging
from typing import List, Dict, Any
from src.logic.agents.compliance.core.ComplianceCore import ComplianceCore, ComplianceIssue

__version__ = VERSION

class ComplianceAgent:
    """Shell agent for continuous compliance and regulatory auditing.
    Coordinates fleet-wide scans and reports violations to the security layer.
    """
    
    def __init__(self) -> None:
        self.core = ComplianceCore()
        self.history: List[Dict[str, Any]] = []

    def perform_audit(self, file_map: Dict[str, str]) -> Dict[str, Any]:
        """Audits a map of file_paths to content."""
        all_issues: List[ComplianceIssue] = []
        
        for path, content in file_map.items():
            issues = self.core.audit_content(content, path)
            all_issues.extend(issues)
            
        score = self.core.aggregate_score(all_issues)
        
        report = {
            "score": score,
            "issue_count": len(all_issues),
            "critical_violations": [i.message for i in all_issues if i.severity == "CRITICAL"],
            "status": "PASS" if score > 0.8 else "FAIL"
        }
        
        self.history.append(report)
        logging.info(f"Compliance Report: Score {score:.2f} ({report['status']})")
        
        return report