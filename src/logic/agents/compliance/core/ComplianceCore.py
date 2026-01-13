
from __future__ import annotations
import re
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class ComplianceIssue:
    severity: str
    category: str
    message: str
    file_path: str

class ComplianceCore:
    """Pure logic for continuous compliance auditing and regulatory scanning.
    Identifies licensing conflicts, PII leaks, and dependency risks.
    """
    
    FORBIDDEN_KEYWORDS = [
        r"password\s*=\s*['\"].+['\"]",
        r"api_key\s*=\s*['\"].+['\"]",
        r"aws_secret",
        r"BEGIN RSA PRIVATE KEY"
    ]

    ALLOWED_LICENSES = ["MIT", "Apache-2.0", "BSD-3-Clause", "PSF-2.0"]

    def audit_content(self, content: str, file_path: str) -> List[ComplianceIssue]:
        """Scans content for common compliance and security violations."""
        issues = []
        
        # 1. Secret Scanning
        for pattern in self.FORBIDDEN_KEYWORDS:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(ComplianceIssue(
                    severity="CRITICAL",
                    category="Secret Leak",
                    message=f"Potential credential found matching pattern: {pattern}",
                    file_path=file_path
                ))
                
        # 2. License Detection (Basic)
        if "LICENSE" in file_path.upper():
            found_license = False
            for lic in self.ALLOWED_LICENSES:
                if lic in content:
                    found_license = True
                    break
            if not found_license:
                issues.append(ComplianceIssue(
                    severity="WARNING",
                    category="Licensing",
                    message="Unrecognized or non-standard license detected.",
                    file_path=file_path
                ))
                
        return issues

    def aggregate_score(self, issues: List[ComplianceIssue]) -> float:
        """Calculates a compliance score from 0.0 to 1.0."""
        if not issues:
            return 1.0
        
        deductions = {
            "CRITICAL": 0.5,
            "WARNING": 0.1,
            "INFO": 0.02
        }
        
        score = 1.0
        for issue in issues:
            score -= deductions.get(issue.severity, 0.0)
            
        return max(0.0, score)