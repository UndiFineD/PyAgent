#!/usr/bin/env python3

"""
SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.
"""

import re
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from .SecurityIssueType import SecurityIssueType
from .SecurityVulnerability import SecurityVulnerability
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

class SecurityCore:
    """Pure logic core for security and safety validation."""
    
    SECURITY_PATTERNS: List[Tuple[str, SecurityIssueType, str, str, str]] = [
        (r'(?i)(password|secret|key|token|auth|pwd)\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded secret or password detected",
         "Use environment variables or a secure vault (e.g., Azure Key Vault)."),
        (r'(?i)(api[_-]?key|access[_-]?key)\s*[:=]\s*[\'"][A-Za-z0-9/+=]{16,}[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded API key detected",
         "Rotate the key and move it to a secure configuration provider."),
        (r"os\.system\s*\([^)]*\+",
         SecurityIssueType.COMMAND_INJECTION, "critical",
         "Insecure shell command construction with string concatenation",
         "Use subprocess with shell=False and pass arguments as a list."),
        (r"ev" + r"al\s*\(",
         SecurityIssueType.INSECURE_DESERIALIZATION, "critical",
         "Use of ev" + "al() is highly dangerous as it can execute arbitrary code",
         "Use ast.literal_eval() for safe parsing or json.loads() for data."),
        (r"random\.(random|randint|choice)\s*\(",
         SecurityIssueType.INSECURE_RANDOM, "medium",
         "Insecure random generator used in a potential security context",
         "Use the 'secrets' module for cryptographically strong random numbers."),
        (r"open\s*\([^)]*\+",
         SecurityIssueType.PATH_TRAVERSAL, "high",
         "Potential path traversal via unsafe file open path construction",
         "Validate file paths using Path.resolve() and ensure they are within expected boundaries."),
    ]

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None

    def _record_finding(self, issue_type: str, severity: str, desc: str) -> None:
        """Records security findings for fleet intelligence (Phase 108)."""
        if self.recorder:
            try:
                self.recorder.record_lesson("security_vulnerability", {
                    "type": issue_type,
                    "severity": severity,
                    "description": desc,
                    "timestamp": time.time()
                })
            except Exception as e:
                logging.debug(f"SecurityCore: Failed to record finding: {e}")

    def scan_content(self, content: str) -> List[SecurityVulnerability]:
        """Performs a comprehensive scan of the provided content."""
        vulnerabilities = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line):
                    vuln = SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix
                    )
                    vulnerabilities.append(vuln)
                    self._record_finding(issue_type.value, severity, desc)
        
        # Add injection scanning
        injection_findings = self.scan_for_injection(content)
        for inf in injection_findings:
             vulnerabilities.append(SecurityVulnerability(
                type=SecurityIssueType.INJECTION_ATTEMPT,
                severity="high",
                description=inf,
                line_number=0,
                fix_suggestion="Sanitize all inputs and wrap specialized instructions in strict boundaries."
            ))
             self._record_finding(SecurityIssueType.INJECTION_ATTEMPT.value, "high", inf)
            
        return vulnerabilities

    def audit_command(self, command: str) -> Tuple[str, str]:
        """Audits a shell command for dangerous operations."""
        risky_patterns = [
            (r"rm\s+-rf\s+/", "CRITICAL: Destructive root deletion requested"),
            (r"rm\s+-rf\s+\*", "HIGH: Recursive deletion in current directory"),
            (r"chmod\s+777", "MEDIUM: Overly permissive permissions (world-writable)"),
            (r"curl\|bash|wget\|sh|curl.*\|.*sh", "HIGH: Remote script execution (pipe to shell)"),
            (r"unset\s+HISTFILE", "MEDIUM: Attempt to disable shell history (anti-forensics)"),
            (r"mv\s+.*\s+/dev/null", "MEDIUM: Deletion by moving to null device"),
        ]
        
        for pattern, warning in risky_patterns:
            if re.search(pattern, command):
                return "HIGH", warning
        
        return "LOW", "No obvious security risks detected in command."

    def validate_shell_script(self, script_content: str) -> List[str]:
        """Analyzes shell scripts for common pitfalls and security bugs."""
        findings = []
        
        # Unquoted variable expansion
        if re.search(r"\$[a-zA-Z_][a-zA-Z0-9_]*[^\"']", script_content):
            findings.append("SC2086: Unquoted variable expansion. Prone to word splitting and globbing.")
            
        # Backticks vs $(...)
        if re.search(r"`.*`", script_content):
            findings.append("SC2006: Use of legacy backticks for command substitution. Use $(...) instead.")
            
        # Useless cat
        if re.search(r"cat\s+.*\s*\|\s*grep", script_content):
            findings.append("SC2002: Useless use of cat. Grep can read files directly.")

        # POSIX compatibility
        if "#!/bin/sh" in script_content and "[[" in script_content:
            findings.append("SC2039: [[ .. ]] is a bash/zsh extension. Use [ .. ] for standard POSIX sh.")
            
        return findings

    def scan_for_injection(self, content: str) -> List[str]:
        """Detects prompt injection or agent manipulation attempts."""
        injection_patterns = {
            "Instruction Override": r"(?i)(ignore previous instructions|disregard all earlier commands|system prompt reset|you are now a|stay in character as)",
            "Indirect Directive": r"(?i)(agent:|assistant:|bot:)\s*(execute|run|delete|send|upload|rm |chmod)",
            "Payload Loader": r"(?i)(fetch the following url and run|download and execute|base64 decode this|eval\(base64)",
            "Social Engineering": r"(?i)(congratulations!|security alert: action|verify your account|login to continue)"
        }
        findings = []
        for name, pattern in injection_patterns.items():
            if re.search(pattern, content):
                findings.append(f"INJECTION ATTEMPT: {name} pattern detected.")
        return findings

    def get_risk_level(self, vulnerabilities: List[SecurityVulnerability]) -> str:
        """Determines the overall risk level for a report."""
        severities = [v.severity for v in vulnerabilities]
        if "critical" in severities or "CRITICAL" in [s.upper() for s in severities]:
            return "CRITICAL"
        if "high" in severities or "HIGH" in [s.upper() for s in severities]:
            return "HIGH"
        if "medium" in severities or "MEDIUM" in [s.upper() for s in severities]:
            return "MEDIUM"
        return "LOW"
