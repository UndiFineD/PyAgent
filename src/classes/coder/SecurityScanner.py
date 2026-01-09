#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .SecurityIssueType import SecurityIssueType
from .SecurityVulnerability import SecurityVulnerability

from base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

class SecurityScanner:
    """Scans code for security vulnerabilities.

    Identifies common security issues and provides remediation guidance.

    Attributes:
        vulnerabilities: List of detected vulnerabilities.

    Example:
        >>> scanner=SecurityScanner()
        >>> vulns=scanner.scan("password='secret123'")
    """

    SECURITY_PATTERNS: List[Tuple[str, SecurityIssueType, str, str, str]] = [
        (r'password\s*=\s*[\'"][^\'"]+[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded password detected",
         "Use environment variables or secure vault"),
        (r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded API key detected",
         "Use environment variables or secure vault"),
        (r"os\.system\s*\([^)]*\+",
         SecurityIssueType.COMMAND_INJECTION, "critical",
         "Potential command injection vulnerability",
         "Use subprocess with shell=False and proper escaping"),
        (r"ev" + r"al\s*\(",
         SecurityIssueType.INSECURE_DESERIALIZATION, "critical",
         "Use of ev" + "al() is dangerous",
         "Avoid ev" + "al() or use ast.literal_eval() for safe parsing"),
        (r"random\.(random|randint|choice)\s*\(",
         SecurityIssueType.INSECURE_RANDOM, "medium",
         "Insecure random number generation for security context",
         "Use secrets module for cryptographic randomness"),
        (r"open\s*\([^)]*\+",
         SecurityIssueType.PATH_TRAVERSAL, "high",
         "Potential path traversal vulnerability",
         "Validate and sanitize file paths"),
    ]

    def __init__(self) -> None:
        """Initialize the security scanner."""
        self.vulnerabilities: List[SecurityVulnerability] = []

    def scan(self, content: str) -> List[SecurityVulnerability]:
        """Scan code for security vulnerabilities.

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
        """
        self.vulnerabilities = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line, re.I):
                    self.vulnerabilities.append(SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix
                    ))

        return self.vulnerabilities

    def get_critical_count(self) -> int:
        """Get count of critical vulnerabilities.

        Returns:
            Number of critical severity vulnerabilities.
        """
        return sum(1 for v in self.vulnerabilities if v.severity == "critical")

