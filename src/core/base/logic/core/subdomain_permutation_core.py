#!/usr/bin/env python3
"""Subdomain permutation core - minimal, parser-safe stub for tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Permutation:
    pattern: str


@dataclass
class PermutationConfig:
    patterns: List[str]


@dataclass
class PermutationResult:
    permutations: List[str]


class SubdomainPermutationCore:
    def __init__(self, config: PermutationConfig) -> None:
        self.config = config

    def generate(self, sub: str, suffix: str) -> List[str]:
        results: List[str] = []
        for p in self.config.patterns:
            results.append(p.replace("{{sub}}", sub).replace("{{suffix}}", suffix))
        return results
