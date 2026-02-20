#!/usr/bin/env python3
"""Minimal cloud asset discovery core used by tests."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CertificateInfo:
    domain: str
    ip_address: str
    port: int
    subject: Dict[str, str]
    issuer: Dict[str, str]
    valid_from: datetime
    valid_until: datetime
    subject_alt_names: List[str]
    organizations: List[str]
    serial_number: str
    signature_algorithm: str


@dataclass
class AssetFinding:
    ip_address: str
    domain: str
    certificate_info: CertificateInfo
    matched_keywords: List[str]
    asset_type: str
    confidence: float
    discovery_method: str


@dataclass
class DiscoveryResult:
    scanned_ips: int
    certificates_found: int
    assets_discovered: List[AssetFinding]
    scan_duration: float
    errors: List[str]


class CloudAssetDiscoveryCore:
    """A small, safe implementation to satisfy imports in tests."""

    def __init__(self, max_concurrent: int = 100, timeout: int = 4):
        self.max_concurrent = max_concurrent
        self.timeout = timeout

    def _init_database(self) -> None:
        # Minimal noop DB init for tests
        return None

    async def discover_assets(
        self,
        ip_ranges: List[str],
        keywords: List[str],
        ports: List[int] | None = None,
        store_certificates: bool = True,
    ) -> DiscoveryResult:
        # Return an empty discovery result to keep tests importable
        return DiscoveryResult(scanned_ips=0, certificates_found=0, assets_discovered=[], scan_duration=0.0, errors=[])


__all__ = ["CertificateInfo", "AssetFinding", "DiscoveryResult", "CloudAssetDiscoveryCore"]
