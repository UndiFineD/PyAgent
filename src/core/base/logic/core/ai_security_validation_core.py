#!/usr/bin/env python3
"""Minimal AI security validation core for tests."""
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


@dataclass
class JailbreakAttempt:
    payload: str
    vector: Optional[str] = None


class AISecurityValidationCore:
    def __init__(self) -> None:
        pass

    def analyze(self, text: str) -> SecurityScanResult:
        return SecurityScanResult(issues=[])


__all__ = ["SecurityIssue", "SecurityScanResult", "JailbreakAttempt", "AISecurityValidationCore"]
