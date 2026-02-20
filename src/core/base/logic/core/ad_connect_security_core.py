#!/usr/bin/env python3
"""Minimal AD Connect security core for tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ADConnectServiceAccount:
    name: str


@dataclass
class ADConnectDatabase:
    connection_string: str


@dataclass
class ADConnectConfiguration:
    version: str = "1.0"


@dataclass
class ADConnectSecurityAssessment:
    issues: List[str]


class ADConnectSecurityCore:
    def __init__(self) -> None:
        self.name = "ADConnectSecurityCore"
        self.version = "1.0.0"
        self.description = "Azure AD Connect Security Analysis and Assessment"

    async def assess(self) -> ADConnectSecurityAssessment:
        return ADConnectSecurityAssessment(issues=[])
