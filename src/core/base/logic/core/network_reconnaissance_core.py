#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Network Reconnaissance Core - Inspired by OWASP Amass patterns
# Provides comprehensive network asset discovery and attack surface mapping

import asyncio
import aiohttp
import dns.resolver
import dns.reversename
import dns.zone
import ipaddress
import json
import re
import ssl
import socket
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from urllib.parse import urlparse, urljoin
import warnings

from src.core.base.common.base_core import BaseCore


@dataclass
class AssetDiscoveryResult:
    """Result of network asset discovery operations."""
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
    """Configuration for reconnaissance operations."""
    max_dns_queries: int = 1000
    rate_limit_delay: float = 0.1
    timeout: int = 10
    max_concurrent_requests: int = 50
    user_agent: str = "PyAgent-NetworkRecon/1.0"
    follow_redirects: bool = True
    verify_ssl: bool = False
    brute_force_subdomains: bool = True
    certificate_analysis: bool = True
    web_crawling: bool = True
    api_discovery: bool = True


class NetworkReconnaissanceCore(BaseCore):
    """
    Network Reconnaissance Core implementing comprehensive asset discovery patterns.

    Inspired by OWASP Amass, this core provides:
    - DNS enumeration and subdomain discovery
    - Certificate transparency analysis
    - Web asset discovery and crawling
    - API endpoint detection
    - Passive and active reconnaissance techniques
    """

    def __init__(self, config: Optional[ReconnaissanceConfig] = None):
        super().__init__()
        self.config = config or ReconnaissanceConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.dns_resolver = dns.resolver.Resolver()
        self.dns_resolver.timeout = self.config.timeout
        self.dns_resolver.lifetime = self.config.timeout

        # Common subdomain wordlists for brute force
        self.subdomain_wordlist = {
            'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
            'blog', 'shop', 'store', 'app', 'mobile', 'web', 'secure', 'ssl',
            'portal', 'login', 'auth', 'oauth', 'sso', 'vpn', 'remote', 'cloud',
            'aws', 'azure', 'gcp', 'cdn', 'static', 'assets', 'media', 'files',
            'download', 'upload', 'backup', 'db', 'database', 'sql', 'mysql',
            'postgres', 'mongo', 'redis', 'cache', 'session', 'api', 'rest',
            'graphql', 'soap', 'ws', 'websocket', 'socket', 'tcp', 'udp'
        }

        # Certificate transparency logs
        self.ct_logs = [
            "https://crt.sh/",
            "https://certspotter.com/api/v1/issuances",
            "https://transparencyreport.google.com/transparencyreport/api/v1.0/certificates/list"
        ]

    async def initialize(self) -> None:
        """Initialize the reconnaissance core."""
        if self.session is None:
            connector = aiohttp.TCPConnector(
                limit=self.config.max_concurrent_requests,
                ttl_dns_cache=300,
                verify_ssl=self.config.verify_ssl
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                headers={'User-Agent': self.config.user_agent},
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )

    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.session:
            await self.session.close()
            self.session = None

    async def discover_assets(self, domain: str) -> AssetDiscoveryResult:
        """
        Perform comprehensive asset discovery for a domain.

        Args:
            domain: Target domain to analyze

        Returns:
            AssetDiscoveryResult with all discovered assets
        """
        await self.initialize()

        result = AssetDiscoveryResult(domain=domain)

        # Run discovery tasks concurrently
        tasks = []

        # DNS enumeration
        tasks.append(self._enumerate_dns(domain, result))

        # Certificate analysis
        if self.config.certificate_analysis:
            tasks.append(self._analyze_certificates(domain, result))

        # Web asset discovery
        if self.config.web_crawling:
            tasks.append(self._discover_web_assets(domain, result))

        # API endpoint discovery
        if self.config.api_discovery:
            tasks.append(self._discover_api_endpoints(domain, result))

        # Brute force subdomains
        if self.config.brute_force_subdomains:
            tasks.append(self._brute_force_subdomains(domain, result))

        # Execute all tasks
        await asyncio.gather(*tasks, return_exceptions=True)

        # Calculate confidence score based on findings
        result.confidence_score = self._calculate_confidence_score(result)

        return result

    async def _enumerate_dns(self, domain: str, result: AssetDiscoveryResult) -> None:
        """Perform DNS enumeration and record collection."""
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SRV', 'NS', 'SOA']

        for record_type in record_types:
            try:
                answers = await asyncio.get_event_loop().run_in_executor(
                    None, self.dns_resolver.resolve, domain, record_type
                )

                records = []
                for answer in answers:
                    if record_type in ['A', 'AAAA']:
                        result.ip_addresses.add(str(answer))
                    records.append(str(answer))

                if records:
                    result.dns_records[record_type] = records

                # Rate limiting
                await asyncio.sleep(self.config.rate_limit_delay)

            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
                continue
            except Exception as e:
                self.logger.warning(f"DNS enumeration error for {domain} {record_type}: {e}")

    async def _brute_force_subdomains(self, domain: str, result: AssetDiscoveryResult) -> None:
        """Brute force subdomain discovery."""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)

        async def check_subdomain(subdomain: str):
            async with semaphore:
                full_domain = f"{subdomain}.{domain}"
                try:
                    answers = await asyncio.get_event_loop().run_in_executor(
                        None, self.dns_resolver.resolve, full_domain, 'A'
                    )

                    if answers:
                        result.subdomains.add(full_domain)
                        for answer in answers:
                            result.ip_addresses.add(str(answer))

                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    pass
                except Exception:
                    pass

                await asyncio.sleep(self.config.rate_limit_delay)

        # Create tasks for all subdomain checks
        tasks = [check_subdomain(sub) for sub in self.subdomain_wordlist]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _analyze_certificates(self, domain: str, result: AssetDiscoveryResult) -> None:
        """Analyze SSL/TLS certificates for subdomains."""
        try:
            # Get certificate from direct connection
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((domain, 443), timeout=self.config.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

                    if cert:
                        cert_info = {
                            'subject': dict(x[0] for x in cert.get('subject', [])),
                            'issuer': dict(x[0] for x in cert.get('issuer', [])),
                            'version': cert.get('version'),
                            'serial_number': str(cert.get('serialNumber', '')),
                            'not_before': cert.get('notBefore'),
                            'not_after': cert.get('notAfter'),
                            'subject_alt_names': cert.get('subjectAltName', [])
                        }
                        result.certificates.append(cert_info)

                        # Extract subdomains from SAN
                        for san_type, san_value in cert.get('subjectAltName', []):
                            if san_type == 'DNS' and san_value.endswith(f'.{domain}'):
                                result.subdomains.add(san_value)

        except Exception as e:
            self.logger.debug(f"Certificate analysis failed for {domain}: {e}")

    async def _discover_web_assets(self, domain: str, result: AssetDiscoveryResult) -> None:
        """Discover web assets through crawling and analysis."""
        if not self.session:
            return

        try:
            # Check main domain
            url = f"https://{domain}"
            async with self.session.get(url, allow_redirects=self.config.follow_redirects) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    result.web_assets.append({
                        'url': str(response.url),
                        'status_code': response.status,
                        'content_type': content_type,
                        'server': response.headers.get('Server', ''),
                        'last_modified': response.headers.get('Last-Modified', ''),
                        'content_length': response.headers.get('Content-Length', '')
                    })

                    # Extract links from HTML if it's HTML content
                    if 'text/html' in content_type:
                        html = await response.text()
                        links = self._extract_links_from_html(html, domain)
                        result.api_endpoints.update(links)

        except Exception as e:
            self.logger.debug(f"Web asset discovery failed for {domain}: {e}")

    async def _discover_api_endpoints(self, domain: str, result: AssetDiscoveryResult) -> None:
        """Discover API endpoints through common patterns."""
        common_endpoints = [
            '/api', '/api/v1', '/api/v2', '/api/v3',
            '/graphql', '/rest', '/soap',
            '/swagger', '/swagger.json', '/openapi.json',
            '/docs', '/documentation', '/api-docs'
        ]

        if not self.session:
            return

        for endpoint in common_endpoints:
            try:
                url = f"https://{domain}{endpoint}"
                async with self.session.get(url, allow_redirects=False) as response:
                    if response.status in [200, 401, 403]:  # API endpoints often return auth errors
                        result.api_endpoints.add(url)

                await asyncio.sleep(self.config.rate_limit_delay)

            except Exception:
                continue

    def _extract_links_from_html(self, html: str, domain: str) -> Set[str]:
        """Extract links from HTML content."""
        links = set()

        # Simple regex patterns for common link extraction
        patterns = [
            r'href=["\']([^"\']+)["\']',
            r'src=["\']([^"\']+)["\']',
            r'action=["\']([^"\']+)["\']'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    # Convert relative URLs to absolute
                    if not match.startswith(('http://', 'https://')):
                        match = urljoin(f"https://{domain}", match)

                    parsed = urlparse(match)
                    if parsed.netloc.endswith(domain):
                        links.add(match)

                except Exception:
                    continue

        return links

    def _calculate_confidence_score(self, result: AssetDiscoveryResult) -> float:
        """Calculate confidence score based on discovery results."""
        score = 0.0

        # Base score for DNS resolution
        if result.ip_addresses:
            score += 0.3

        # Subdomain discovery
        if result.subdomains:
            score += min(len(result.subdomains) * 0.1, 0.3)

        # Certificate analysis
        if result.certificates:
            score += 0.2

        # Web assets
        if result.web_assets:
            score += 0.1

        # API endpoints
        if result.api_endpoints:
            score += 0.1

        return min(score, 1.0)

    async def passive_reconnaissance(self, domain: str) -> AssetDiscoveryResult:
        """
        Perform passive reconnaissance using certificate transparency and DNS.

        Args:
            domain: Target domain

        Returns:
            AssetDiscoveryResult with passive findings
        """
        result = AssetDiscoveryResult(domain=domain)

        # Certificate transparency analysis
        if self.config.certificate_analysis:
            await self._analyze_certificates(domain, result)

        # DNS enumeration (passive)
        await self._enumerate_dns(domain, result)

        result.confidence_score = self._calculate_confidence_score(result)
        return result

    async def active_reconnaissance(self, domain: str) -> AssetDiscoveryResult:
        """
        Perform active reconnaissance including brute force and web crawling.

        Args:
            domain: Target domain

        Returns:
            AssetDiscoveryResult with active findings
        """
        result = AssetDiscoveryResult(domain=domain)

        # Run all active discovery methods
        tasks = [
            self._brute_force_subdomains(domain, result),
            self._discover_web_assets(domain, result),
            self._discover_api_endpoints(domain, result)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

        result.confidence_score = self._calculate_confidence_score(result)
        return result

    def get_discovery_summary(self, result: AssetDiscoveryResult) -> Dict[str, Any]:
        """
        Generate a summary of discovery results.

        Args:
            result: AssetDiscoveryResult to summarize

        Returns:
            Dictionary with summary statistics
        """
        return {
            'domain': result.domain,
            'total_subdomains': len(result.subdomains),
            'total_ip_addresses': len(result.ip_addresses),
            'total_certificates': len(result.certificates),
            'total_web_assets': len(result.web_assets),
            'total_api_endpoints': len(result.api_endpoints),
            'confidence_score': result.confidence_score,
            'discovered_at': result.discovered_at.isoformat(),
            'dns_record_types': list(result.dns_records.keys())
        }