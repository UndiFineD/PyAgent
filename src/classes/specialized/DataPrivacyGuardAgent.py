import re
from typing import Dict, List, Any
from src.classes.base_agent import BaseAgent

class DataPrivacyGuardAgent(BaseAgent):
    """
    Data Privacy Guard Agent: Monitors fleet communications for PII (Personally 
    Identifiable Information), performs redaction, and tracks compliance.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.pii_patterns = {
            "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "Phone": r"\b(?:\d{3}[-.]?)?\d{3}[-.]?\d{4}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "CreditCard": r"\b(?:\d[ -]*?){13,16}\b"
        }
        self.redaction_logs = []

    def scan_and_redact(self, text: str) -> Dict[str, Any]:
        """Scans text for PII patterns and returns redacted version."""
        original_text = text
        redacted_text = text
        findings = []

        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    findings.append({"type": pii_type, "value": match})
                    redacted_text = redacted_text.replace(match, f"[REDACTED_{pii_type.upper()}]")

        if findings:
            self.redaction_logs.append({
                "timestamp": "2026-01-08", # Simulated
                "findings_count": len(findings),
                "pii_types": list(set(f['type'] for f in findings))
            })

        return {
            "original": original_text,
            "redacted": redacted_text,
            "pii_detected": len(findings) > 0,
            "findings": findings
        }

    def verify_message_safety(self, message: str) -> bool:
        """Returns True if no PII is detected, False otherwise."""
        result = self.scan_and_redact(message)
        return not result['pii_detected']

    def get_privacy_metrics(self) -> Dict[str, Any]:
        """Returns summary metrics for privacy protection efforts."""
        return {
            "total_redactions": len(self.redaction_logs),
            "pii_types_captured": list(set(t for log in self.redaction_logs for t in log['pii_types'])),
            "safety_rating": "High" if len(self.redaction_logs) < 100 else "Critical Levels of PII Exposure"
        }
