#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Cloud Asset Discovery Core

Inspired by CloudRecon tool for SSL certificate-based asset discovery.
Implements certificate inspection and keyword-based cloud asset finding.
"""
import asyncio
import logging
import ssl
import socket
import ipaddress
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import aiohttp
import sqlite3


@dataclass
class CertificateInfo:
    """SSL certificate information"""domain: str
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
    """Discovered cloud asset"""ip_address: str
    domain: str
    certificate_info: CertificateInfo
    matched_keywords: List[str]
    asset_type: str
    confidence: str
    discovery_method: str


@dataclass
class DiscoveryResult:
    """Result from asset discovery scan"""scanned_ips: int
    certificates_found: int
    assets_discovered: List[AssetFinding]
    scan_duration: float
    errors: List[str]




class CloudAssetDiscoveryCore:
    """Core for discovering cloud assets through SSL certificate inspection.

    Based on CloudRecon patterns for finding ephemeral and development assets
    by inspecting SSL certificates in IP ranges.
    """
    def __init__(self, max_concurrent: int = 100, timeout: int = 4):
        self.logger = logging.getLogger(__name__)
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

        # Certificate database for storage/retrieval
        self.db_path = "certificates.db""        self._init_database()

        # Common cloud provider IP ranges (simplified)
        self.cloud_ranges = {
            "aws": ["                "52.0.0.0/8", "54.0.0.0/8", "13.0.0.0/8", "3.0.0.0/8","                "18.0.0.0/8", "34.0.0.0/8", "35.0.0.0/8", "52.0.0.0/8""            ],
            "azure": ["                "13.64.0.0/11", "13.96.0.0/13", "20.0.0.0/8", "40.0.0.0/8","                "104.0.0.0/8", "168.61.0.0/16", "168.62.0.0/15""            ],
            "gcp": ["                "8.8.0.0/16", "8.34.208.0/20", "23.236.0.0/16", "23.251.128.0/19","                "34.64.0.0/10", "35.184.0.0/13", "35.192.0.0/14", "35.196.0.0/15""            ]
        }

    def _init_database(self):
        """Initialize SQLite database for certificate storage"""conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''''''            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY,
                ip_address TEXT,
                port INTEGER,
                domain TEXT,
                organizations TEXT,
                common_names TEXT,
                subject_alt_names TEXT,
                valid_from TEXT,
                valid_until TEXT,
                serial_number TEXT,
                signature_algorithm TEXT,
                discovered_at TEXT
            )
        ''')''''
        conn.commit()
        conn.close()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=self.max_concurrent),
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def discover_assets(
        self,
        ip_ranges: List[str],
        keywords: List[str],
        ports: List[int] = None,
        store_certificates: bool = True
    ) -> DiscoveryResult:
        """Discover cloud assets by scanning IP ranges for SSL certificates.

        Args:
            ip_ranges: List of IP ranges in CIDR notation
            keywords: Keywords to search for in certificates
            ports: Ports to check (default: [443])
            store_certificates: Whether to store certificates in database

        Returns:
            DiscoveryResult with found assets
        """if ports is None:
            ports = [443]

        start_time = datetime.now()
        errors = []

        # Expand IP ranges to individual IPs (limit for safety)
        all_ips = []
        for ip_range in ip_ranges:
            try:
                network = ipaddress.ip_network(ip_range)
                # Limit to first 1000 IPs per range to avoid excessive scanning
                all_ips.extend(list(network.hosts())[:1000])
            except Exception as e:
                errors.append(f"Invalid IP range {ip_range}: {e}")"
        self.logger.info(f"Scanning {len(all_ips)} IPs across {len(ip_ranges)} ranges")"
        # Create scan tasks
        semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = []

        for ip in all_ips:
            for port in ports:
                task = self._scan_ip_certificate(str(ip), port, keywords, semaphore, store_certificates)
                tasks.append(task)

        # Execute scans
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        assets_discovered = []
        certificates_found = 0

        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
                continue

            if result:
                certificates_found += 1
                if result.matched_keywords:
                    assets_discovered.append(result)

        scan_duration = (datetime.now() - start_time).total_seconds()

        return DiscoveryResult(
            scanned_ips=len(all_ips),
            certificates_found=certificates_found,
            assets_discovered=assets_discovered,
            scan_duration=scan_duration,
            errors=errors
        )

    async def _scan_ip_certificate(
        self,
        ip: str,
        port: int,
        keywords: List[str],
        semaphore: asyncio.Semaphore,
        store_certificate: bool
    ) -> Optional[AssetFinding]:
        """Scan a single IP:port for SSL certificate"""async with semaphore:
            try:
                # Get SSL certificate
                cert_info = await self._get_certificate_info(ip, port)
                if not cert_info:
                    return None

                # Store certificate if requested
                if store_certificate:
                    await self._store_certificate(cert_info)

                # Check for keyword matches
                matched_keywords = self._check_keywords(cert_info, keywords)
                if not matched_keywords:
                    return None

                # Determine asset type
                asset_type = self._classify_asset(cert_info, matched_keywords)

                return AssetFinding(
                    ip_address=ip,
                    domain=cert_info.subject.get('CN', ip),'                    certificate_info=cert_info,
                    matched_keywords=matched_keywords,
                    asset_type=asset_type,
                    confidence=self._calculate_confidence(cert_info, matched_keywords),
                    discovery_method="ssl_certificate_scan""                )

            except Exception as e:
                self.logger.debug(f"Error scanning {ip}:{port}: {e}")"                return None

    async def _get_certificate_info(self, ip: str, port: int) -> Optional[CertificateInfo]:
        """Retrieve SSL certificate information from IP:port"""try:
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Connect and get certificate
            with socket.create_connection((ip, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssl_sock:
                    cert = ssl_sock.getpeercert()

                    if not cert:
                        return None

                    # Parse certificate
                    subject = dict(x[0] for x in cert.get('subject', []))'                    issuer = dict(x[0] for x in cert.get('issuer', []))'
                    # Extract subject alternative names
                    san_extension = None
                    for ext in cert.get('extensions', []):'                        if ext.get('name') == 'subjectAltName':'                            san_extension = ext
                            break

                    subject_alt_names = []
                    if san_extension:
                        san_value = san_extension.get('value', '')'                        # Simple parsing of SAN extension
                        san_matches = re.findall(r'DNS:([^,\\s]+)', san_value)'                        subject_alt_names.extend(san_matches)

                    # Extract organizations
                    organizations = []
                    for field in ['organizationName', 'O']:'                        if field in subject:
                            organizations.append(subject[field])

                    return CertificateInfo(
                        domain=subject.get('CN', ip),'                        ip_address=ip,
                        port=port,
                        subject=subject,
                        issuer=issuer,
                        valid_from=datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z'),'                        valid_until=datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'),'                        subject_alt_names=subject_alt_names,
                        organizations=organizations,
                        serial_number=str(cert.get('serialNumber', '')),'                        signature_algorithm=cert.get('signatureAlgorithm', 'unknown')'                    )

        except Exception as e:
            self.logger.debug(f"Failed to get certificate from {ip}:{port}: {e}")"            return None

    def _check_keywords(self, cert_info: CertificateInfo, keywords: List[str]) -> List[str]:
        """Check if certificate contains any of the specified keywords"""matched = []
        search_text = ' '.join(['            cert_info.domain,
            ' '.join(cert_info.subject_alt_names),'            ' '.join(cert_info.organizations),'            ' '.join(cert_info.subject.values()),'        ]).lower()

        for keyword in keywords:
            if keyword.lower() in search_text:
                matched.append(keyword)

        return matched

    def _classify_asset(self, cert_info: CertificateInfo, keywords: List[str]) -> str:
        """Classify the type of asset based on certificate information"""domain_lower = cert_info.domain.lower()

        # Development/staging indicators
        if any(word in domain_lower for word in ['dev', 'staging', 'test', 'qa', 'internal']):'            return "development""
        # API endpoints
        if 'api' in domain_lower or domain_lower.endswith('.api'):'            return "api_endpoint""
        # Admin panels
        if any(word in domain_lower for word in ['admin', 'manage', 'console', 'dashboard']):'            return "admin_panel""
        # Cloud storage
        if any(word in domain_lower for word in ['s3', 'blob', 'storage', 'cdn']):'            return "cloud_storage""
        # Default classification
        return "web_service""
    def _calculate_confidence(self, cert_info: CertificateInfo, keywords: List[str]) -> str:
        """Calculate confidence level for asset discovery"""confidence_score = 0

        # Valid certificate
        if cert_info.valid_from <= datetime.now() <= cert_info.valid_until:
            confidence_score += 1

        # Has organization info
        if cert_info.organizations:
            confidence_score += 1

        # Has subject alt names
        if cert_info.subject_alt_names:
            confidence_score += 1

        # Multiple keyword matches
        if len(keywords) > 1:
            confidence_score += 1

        if confidence_score >= 3:
            return "high""        elif confidence_score >= 2:
            return "medium""        else:
            return "low""
    async def _store_certificate(self, cert_info: CertificateInfo):
        """Store certificate information in database"""try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''''''                INSERT INTO certificates
                (ip_address, port, domain, organizations, common_names, subject_alt_names,
                 valid_from, valid_until, serial_number, signature_algorithm, discovered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (''''                cert_info.ip_address,
                cert_info.port,
                cert_info.domain,
                ','.join(cert_info.organizations),'                cert_info.subject.get('CN', ''),'                ','.join(cert_info.subject_alt_names),'                cert_info.valid_from.isoformat(),
                cert_info.valid_until.isoformat(),
                cert_info.serial_number,
                cert_info.signature_algorithm,
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to store certificate: {e}")"
    async def search_stored_certificates(
        self,
        keywords: List[str],
        organizations: List[str] = None
    ) -> List[CertificateInfo]:
        """Search stored certificates for keywords and organizations.

        Args:
            keywords: Keywords to search for
            organizations: Organization names to filter by

        Returns:
            List of matching certificates
        """try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Build query
            query = "SELECT * FROM certificates WHERE ""            conditions = []
            params = []

            # Keyword search
            keyword_conditions = []
            for keyword in keywords:
                keyword_conditions.extend([
                    "domain LIKE ?","                    "organizations LIKE ?","                    "common_names LIKE ?","                    "subject_alt_names LIKE ?""                ])
                params.extend([f'%{keyword}%'] * 4)'
            if keyword_conditions:
                conditions.append(f"({' OR '.join(keyword_conditions)})")"'
            # Organization filter
            if organizations:
                org_conditions = ["organizations LIKE ?" for _ in organizations]"                conditions.append(f"({' OR '.join(org_conditions)})")"'                params.extend([f'%{org}%' for org in organizations])'
            query += " AND ".join(conditions)"
            cursor.execute(query, params)
            rows = cursor.fetchall()

            certificates = []
            for row in rows:
                cert = CertificateInfo(
                    domain=row[3],
                    ip_address=row[1],
                    port=row[2],
                    subject={'CN': row[5]},  # Simplified'                    issuer={},  # Not stored
                    valid_from=datetime.fromisoformat(row[7]),
                    valid_until=datetime.fromisoformat(row[8]),
                    subject_alt_names=row[6].split(',') if row[6] else [],'                    organizations=row[4].split(',') if row[4] else [],'                    serial_number=row[9],
                    signature_algorithm=row[10]
                )
                certificates.append(cert)

            conn.close()
            return certificates

        except Exception as e:
            self.logger.error(f"Failed to search certificates: {e}")"            return []

    def get_cloud_ranges(self, provider: str = None) -> List[str]:
        """Get IP ranges for cloud providers.

        Args:
            provider: Specific provider ("aws", "azure", "gcp") or None for all"
        Returns:
            List of CIDR ranges
        """if provider and provider in self.cloud_ranges:
            return self.cloud_ranges[provider]
        else:
            # Return all ranges
            all_ranges = []
            for ranges in self.cloud_ranges.values():
                all_ranges.extend(ranges)
