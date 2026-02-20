#!/usr/bin/env python3
"""Minimal, parser-safe Subdomain Permutation Core used for tests."""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Permutation:
    pattern: str


@dataclass
class PermutationConfig:
    patterns: List[str]


class SubdomainPermutationCore:
    def __init__(self, config: PermutationConfig):
        self.config = config

    def generate(self, sub: str, suffix: str) -> List[str]:
        results = []
        for p in self.config.patterns:
            results.append(p.replace("{{sub}}", sub).replace("{{suffix}}", suffix))
        return results
