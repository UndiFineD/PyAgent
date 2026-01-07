#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ChangelogEntry import ChangelogEntry
from .ComplianceCategory import ComplianceCategory
from .ComplianceResult import ComplianceResult

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class ComplianceChecker:
    """Checks changelog compliance with various requirements.

    Verifies changelog entries meet security, legal, and
    other compliance requirements.

    Example:
        >>> checker=ComplianceChecker()
        >>> results=checker.check_all(entries)
    """

    SECURITY_KEYWORDS = ["vulnerability", "cve", "security", "patch", "exploit"]
    LEGAL_KEYWORDS = ["license", "copyright", "trademark", "patent"]

    def check_security_compliance(self, entries: List[ChangelogEntry]) -> ComplianceResult:
        """Check security compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for security category.
        """
        issues: List[str] = []
        recommendations: List[str] = []
        # Check for security entries without proper categorization
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.SECURITY_KEYWORDS):
                if entry.category != "Security":
                    issues.append(
                        f"Security-related entry not in Security category: "
                        f"{entry.description[:50]}"
                    )
                    recommendations.append("Move security-related entries to the Security section")
        return ComplianceResult(
            category=ComplianceCategory.SECURITY,
            passed=len(issues) == 0,
            issues=issues,
            recommendations=recommendations
        )

    def check_legal_compliance(self, entries: List[ChangelogEntry]) -> ComplianceResult:
        """Check legal compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for legal category.
        """
        issues: List[str] = []
        recommendations: List[str] = []
        # Check for entries that may need legal review
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.LEGAL_KEYWORDS):
                issues.append(f"Entry may need legal review: {entry.description[:50]}")
                recommendations.append("Have legal team review license / copyright changes")
        return ComplianceResult(
            category=ComplianceCategory.LEGAL,
            passed=len(issues) == 0,
            issues=issues,
            recommendations=recommendations
        )

    def check_all(self, entries: List[ChangelogEntry]) -> List[ComplianceResult]:
        """Run all compliance checks.

        Args:
            entries: Changelog entries to check.

        Returns:
            List of ComplianceResult for all categories.
        """
        return [
            self.check_security_compliance(entries),
            self.check_legal_compliance(entries)
        ]
