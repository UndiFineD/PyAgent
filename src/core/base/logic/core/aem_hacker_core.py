#!/usr/bin/env python3
"""Minimal AEM hacker core for tests.

Provides lightweight dataclasses and a simple core
implementation sufficient for unit tests to import.
"""
try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import List, Optional
except ImportError:
    from typing import List, Optional



@dataclass
class AEMFinding:
    path: str
    severity: str = "medium"
    cve: Optional[str] = None


@dataclass
class AEMScanConfig:
    target: str
    user_agent: str = "pyagent-test"


@dataclass
class AEMScanResults:
    findings: List[AEMFinding]


class AEMSSRFDetector:
    def __init__(self, token: str | None = None) -> None:
        self.token = token

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None


class AEMSSRFHandler:
    def handle(self, finding: AEMFinding) -> None:
        pass


class AEMHackerCore:
    def __init__(self, config: AEMScanConfig | None = None) -> None:
        self.config = config or AEMScanConfig(target="localhost")

    async def perform_aem_assessment(self, config: AEMScanConfig | None = None):
        cfg = config or self.config
        return AEMScanResults(findings=[])


__all__ = [
    "AEMFinding",
    "AEMScanConfig",
    "AEMScanResults",
    "AEMSSRFDetector",
    "AEMSSRFHandler",
    "AEMHackerCore",
]
