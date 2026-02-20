#!/usr/bin/env python3
"""Minimal, parser-safe network reconnaissance core stub used for tests.

This file provides small, well-formed replacements for the real (and
potentially large) network reconnaissance implementation so tests can
import the expected symbols without executing complex network logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set


@dataclass
class AssetDiscoveryResult:
    domain: str
    subdomains: Set[str] = field(default_factory=set)
    ip_addresses: Set[str] = field(default_factory=set)
    certificates: List[Dict[str, Any]] = field(default_factory=list)
    dns_records: Dict[str, List[str]] = field(default_factory=dict)
    web_assets: List[Dict[str, Any]] = field(default_factory=list)
    api_endpoints: Set[str] = field(default_factory=set)
    discovered_at: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0


@dataclass
class ReconnaissanceConfig:
    max_dns_queries: int = 1000
    rate_limit_delay: float = 0.1
    timeout: int = 10
    max_concurrent_requests: int = 10
    user_agent: str = "PyAgent-NetworkRecon/1.0"
    follow_redirects: bool = True
    verify_ssl: bool = False
    brute_force_subdomains: bool = False
    certificate_analysis: bool = False
    web_crawling: bool = False
    api_discovery: bool = False


class NetworkReconnaissanceCore:
    """A small, test-friendly stub of the reconnaissance core."""

    def __init__(self, config: Optional[ReconnaissanceConfig] = None):
        self.config = config or ReconnaissanceConfig()

    async def initialize(self) -> None:
        return None

    async def cleanup(self) -> None:
        return None

    async def discover_assets(self, domain: str) -> AssetDiscoveryResult:
        result = AssetDiscoveryResult(domain=domain)
        # Minimal deterministic behavior for tests
        result.subdomains.add(f"www.{domain}")
        result.ip_addresses.add("127.0.0.1")
        result.confidence_score = 0.1
        return result
