#!/usr/bin/env python3
"""Minimal stub for ai_security_validation_core used during repairs."""

from __future__ import annotations


class AISecurityValidationCore:
    """Repair-time stub of AISecurityValidationCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["AISecurityValidationCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: AI security validation core (conservative).

Minimal stub to keep imports working and preserve basic types.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SecurityIssue:
    id: str
    description: str
    severity: str = "medium"


@dataclass
class SecurityScanResult:
    issues: List[SecurityIssue]


class AISecurityValidationCore:
    def analyze(self, text: str) -> SecurityScanResult:
        return SecurityScanResult(issues=[])


__all__ = ["SecurityIssue", "SecurityScanResult", "AISecurityValidationCore"]
