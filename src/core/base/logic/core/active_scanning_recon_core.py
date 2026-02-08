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

"""
Active Scanning and Reconnaissance Core

Inspired by active-scan-plus-plus repository patterns for comprehensive
network scanning, service enumeration, and vulnerability assessment.
"""

import asyncio
import logging
import socket
import ssl
import json
import ipaddress
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


@dataclass
class ScanTarget:
    """Target for scanning operations"""
    ip_address: str
    hostname: Optional[str] = None
    ports: List[int] = None
    services: Dict[int, str] = None
    vulnerabilities: List[Dict[str, Any]] = None
    last_scanned: Optional[datetime] = None

    def __post_init__(self):
        if self.ports is None:
            self.ports = []
        if self.services is None:
            self.services = {}
        if self.vulnerabilities is None:
            self.vulnerabilities = []


@dataclass
class ScanResult:
    """Result from scanning operation"""
    target: ScanTarget
    scan_type: str
    findings: List[Dict[str, Any]]
    scan_duration: float
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


@dataclass
class VulnerabilityFinding:
    """Vulnerability finding"""
    cve_id: Optional[str]
    severity: str
    description: str
    affected_service: str
    port: int
    exploit_available: bool
    cvss_score: Optional[float]
    remediation: str


class ActiveScanningReconCore:
    """
    Core for active scanning and reconnaissance operations.

    Based on patterns from active-scan-plus-plus repository, implementing
    comprehensive network scanning, service enumeration, and vulnerability assessment.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Common ports to scan
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
            1723, 3306, 3389, 5900, 8080, 8443
        ]

        # Service signatures
        self.service_signatures = self._init_service_signatures()

        # Vulnerability database (simplified)
        self.vuln_db = self._init_vulnerability_db()

        # Scan configuration
        self.max_concurrent_scans = 100
        self.scan_timeout = 5.0
        self.thread_pool = ThreadPoolExecutor(max_workers=50)

    def _init_service_signatures(self) -> Dict[str, Dict[str, Any]]:
        """Initialize service detection signatures"""
        return {
            "http": {
                "ports": [80, 8080, 8443],
                "signature": b"HTTP/",
                "description": "HTTP Web Server"
            },
            "https": {
                "ports": [443, 8443],
                "signature": b"HTTP/",
                "description": "HTTPS Web Server",
                "ssl": True
            },
            "ssh": {
                "ports": [22],
                "signature": b"SSH-",
                "description": "SSH Server"
            },
            "ftp": {
                "ports": [21],
                "signature": b"220",
                "description": "FTP Server"
            },
            "smtp": {
                "ports": [25],
                "signature": b"220",
                "description": "SMTP Server"
            },
            "mysql": {
                "ports": [3306],
                "signature": b"\x0a\x35\x2e",
                "description": "MySQL Database"
            },
            "rdp": {
                "ports": [3389],
                "signature": b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x1f\x08\x00\x08\x00\x00\x00\x00\x00",
                "description": "Remote Desktop Protocol"
            }
        }

    def _init_vulnerability_db(self) -> Dict[str, List[VulnerabilityFinding]]:
        """Initialize simplified vulnerability database"""
        return {
            "apache": [
                VulnerabilityFinding(
                    cve_id="CVE-2021-41773",
                    severity="high",
                    description="Path traversal vulnerability in Apache HTTP Server",
                    affected_service="Apache",
                    port=80,
                    exploit_available=True,
                    cvss_score=7.5,
                    remediation="Upgrade to Apache 2.4.49 or later"
                )
            ],
            "nginx": [
                VulnerabilityFinding(
                    cve_id="CVE-2021-23017",
                    severity="medium",
                    description="Off-by-one error in nginx range filter",
                    affected_service="nginx",
                    port=80,
                    exploit_available=False,
                    cvss_score=5.3,
                    remediation="Upgrade to nginx 1.21.1 or later"
                )
            ],
            "openssh": [
                VulnerabilityFinding(
                    cve_id="CVE-2020-14145",
                    severity="medium",
                    description="User enumeration via challenge response",
                    affected_service="OpenSSH",
                    port=22,
                    exploit_available=False,
                    cvss_score=5.3,
                    remediation="Upgrade to OpenSSH 8.4 or later"
                )
            ]
        }

    async def comprehensive_scan(self, targets: List[str],
                               scan_types: List[str] = None) -> List[ScanResult]:
        """
        Perform comprehensive scanning on multiple targets.

        Args:
            targets: List of IP addresses or hostnames to scan
            scan_types: Types of scans to perform (port, service, vuln)

        Returns:
            List of scan results
        """
        if scan_types is None:
            scan_types = ["port", "service", "vuln"]

        results = []

        # Convert targets to ScanTarget objects
        scan_targets = []
        for target in targets:
            try:
                # Validate IP address
                ipaddress.ip_address(target)
                scan_targets.append(ScanTarget(ip_address=target))
            except ValueError:
                # Try to resolve hostname
                try:
                    ip = socket.gethostbyname(target)
                    scan_targets.append(ScanTarget(ip_address=ip, hostname=target))
                except socket.gaierror:
                    self.logger.warning(f"Could not resolve target: {target}")
                    continue

        # Perform scans based on type
        for scan_type in scan_types:
            if scan_type == "port":
                port_results = await self._port_scan(scan_targets)
                results.extend(port_results)
            elif scan_type == "service":
                service_results = await self._service_scan(scan_targets)
                results.extend(service_results)
            elif scan_type == "vuln":
                vuln_results = await self._vulnerability_scan(scan_targets)
                results.extend(vuln_results)

        return results

    async def _port_scan(self, targets: List[ScanTarget]) -> List[ScanResult]:
        """Perform port scanning on targets"""
        results = []

        semaphore = asyncio.Semaphore(self.max_concurrent_scans)

        async def scan_target_ports(target: ScanTarget) -> ScanResult:
            async with semaphore:
                start_time = datetime.now()
                open_ports = []

                try:
                    # Scan common ports
                    for port in self.common_ports:
                        if await self._is_port_open(target.ip_address, port):
                            open_ports.append(port)

                    # Update target with found ports
                    target.ports = open_ports
                    target.last_scanned = datetime.now()

                    findings = [{"port": port, "state": "open"} for port in open_ports]

                    scan_duration = (datetime.now() - start_time).total_seconds()

                    return ScanResult(
                        target=target,
                        scan_type="port_scan",
                        findings=findings,
                        scan_duration=scan_duration,
                        timestamp=datetime.now(),
                        success=True
                    )

                except Exception as e:
                    scan_duration = (datetime.now() - start_time).total_seconds()
                    return ScanResult(
                        target=target,
                        scan_type="port_scan",
                        findings=[],
                        scan_duration=scan_duration,
                        timestamp=datetime.now(),
                        success=False,
                        error_message=str(e)
                    )

        # Run port scans concurrently
        tasks = [scan_target_ports(target) for target in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return results
        valid_results = [r for r in results if isinstance(r, ScanResult)]
        return valid_results

    async def _is_port_open(self, ip: str, port: int) -> bool:
        """Check if a port is open on target"""
        try:
            loop = asyncio.get_event_loop()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_timeout)
            sock.setblocking(False)

            # Attempt connection
            await loop.sock_connect(sock, (ip, port))
            sock.close()
            return True

        except (asyncio.TimeoutError, OSError):
            return False

    async def _service_scan(self, targets: List[ScanTarget]) -> List[ScanResult]:
        """Perform service enumeration on targets"""
        results = []

        async def scan_target_services(target: ScanTarget) -> ScanResult:
            start_time = datetime.now()
            services_found = {}

            try:
                # Scan each open port for service identification
                for port in target.ports:
                    service = await self._identify_service(target.ip_address, port)
                    if service:
                        services_found[port] = service
                        target.services[port] = service

                findings = [
                    {"port": port, "service": service}
                    for port, service in services_found.items()
                ]

                scan_duration = (datetime.now() - start_time).total_seconds()

                return ScanResult(
                    target=target,
                    scan_type="service_scan",
                    findings=findings,
                    scan_duration=scan_duration,
                    timestamp=datetime.now(),
                    success=True
                )

            except Exception as e:
                scan_duration = (datetime.now() - start_time).total_seconds()
                return ScanResult(
                    target=target,
                    scan_type="service_scan",
                    findings=[],
                    scan_duration=scan_duration,
                    timestamp=datetime.now(),
                    success=False,
                    error_message=str(e)
                )

        # Run service scans concurrently
        tasks = [scan_target_services(target) for target in targets if target.ports]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, ScanResult)]
        return valid_results

    async def _identify_service(self, ip: str, port: int) -> Optional[str]:
        """Identify service running on port"""
        try:
            loop = asyncio.get_event_loop()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_timeout)
            sock.setblocking(False)

            await loop.sock_connect(sock, (ip, port))

            # Try SSL/TLS first for common SSL ports
            if port in [443, 8443, 993, 995]:
                try:
                    ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
                    ssl_sock.settimeout(self.scan_timeout)
                    service = await self._identify_ssl_service(ssl_sock, port)
                    ssl_sock.close()
                    return service
                except ssl.SSLError:
                    pass  # Fall back to plain connection

            # Send probe and read response
            probe_data = b"HEAD / HTTP/1.0\r\n\r\n" if port in [80, 8080] else b"\r\n"
            await loop.sock_sendall(sock, probe_data)

            response = await loop.sock_recv(sock, 1024)
            sock.close()

            # Match against service signatures
            for service_name, signature in self.service_signatures.items():
                if port in signature["ports"] and signature["signature"] in response:
                    return signature["description"]

            # Fallback: try banner grabbing
            return await self._grab_banner(ip, port)

        except (asyncio.TimeoutError, OSError):
            return None

    async def _identify_ssl_service(self, ssl_sock: ssl.SSLSocket, port: int) -> Optional[str]:
        """Identify service over SSL/TLS"""
        try:
            # Perform SSL handshake
            ssl_sock.do_handshake()

            # Send HTTP request for web services
            if port in [443, 8443]:
                ssl_sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                response = ssl_sock.recv(1024)
                if b"HTTP/" in response:
                    return "HTTPS Web Server"

            # For other SSL services, check certificate
            cert = ssl_sock.getpeercert()
            if cert:
                return f"SSL/TLS Service (Port {port})"

        except Exception:
            pass

        return None

    async def _grab_banner(self, ip: str, port: int) -> Optional[str]:
        """Perform banner grabbing to identify service"""
        try:
            loop = asyncio.get_event_loop()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_timeout)
            sock.setblocking(False)

            await loop.sock_connect(sock, (ip, port))

            # Send minimal probe
            await loop.sock_sendall(sock, b"\r\n")
            banner = await loop.sock_recv(sock, 256)
            sock.close()

            # Simple banner analysis
            banner_str = banner.decode('utf-8', errors='ignore').strip()

            if banner_str.startswith("220"):
                return "FTP Server" if "FTP" in banner_str else "SMTP Server"
            elif "SSH" in banner_str:
                return "SSH Server"
            elif "MySQL" in banner_str:
                return "MySQL Database"

            return f"Unknown Service (Banner: {banner_str[:50]})"

        except Exception:
            return None

    async def _vulnerability_scan(self, targets: List[ScanTarget]) -> List[ScanResult]:
        """Perform vulnerability scanning on targets"""
        results = []

        async def scan_target_vulns(target: ScanTarget) -> ScanResult:
            start_time = datetime.now()
            vulnerabilities = []

            try:
                # Check each identified service for known vulnerabilities
                for port, service in target.services.items():
                    service_vulns = self._check_service_vulnerabilities(service, port)
                    vulnerabilities.extend(service_vulns)

                # Update target with vulnerabilities
                target.vulnerabilities = [vars(vuln) for vuln in vulnerabilities]

                findings = [vars(vuln) for vuln in vulnerabilities]

                scan_duration = (datetime.now() - start_time).total_seconds()

                return ScanResult(
                    target=target,
                    scan_type="vulnerability_scan",
                    findings=findings,
                    scan_duration=scan_duration,
                    timestamp=datetime.now(),
                    success=True
                )

            except Exception as e:
                scan_duration = (datetime.now() - start_time).total_seconds()
                return ScanResult(
                    target=target,
                    scan_type="vulnerability_scan",
                    findings=[],
                    scan_duration=scan_duration,
                    timestamp=datetime.now(),
                    success=False,
                    error_message=str(e)
                )

        # Run vulnerability scans
        tasks = [scan_target_vulns(target) for target in targets if target.services]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, ScanResult)]
        return valid_results

    def _check_service_vulnerabilities(self, service: str, port: int) -> List[VulnerabilityFinding]:
        """Check for vulnerabilities in a service"""
        vulnerabilities = []
        service_lower = service.lower()

        # Check vulnerability database
        for vuln_service, vulns in self.vuln_db.items():
            if vuln_service in service_lower:
                for vuln in vulns:
                    if vuln.port == port:
                        vulnerabilities.append(vuln)

        return vulnerabilities

    async def network_discovery(self, ip_range: str) -> List[ScanTarget]:
        """
        Perform network discovery on IP range.

        Args:
            ip_range: CIDR notation (e.g., "192.168.1.0/24")

        Returns:
            List of discovered targets
        """
        try:
            network = ipaddress.ip_network(ip_range)
            targets = []

            # Ping sweep (simplified - just check if host responds)
            for ip in network.hosts():
                if await self._host_discovery(str(ip)):
                    target = ScanTarget(ip_address=str(ip))
                    targets.append(target)

            return targets

        except ValueError as e:
            self.logger.error(f"Invalid IP range: {ip_range} - {e}")
            return []

    async def _host_discovery(self, ip: str) -> bool:
        """Check if host is alive (simplified ping)"""
        try:
            # Try to connect to a common port as host discovery
            return await self._is_port_open(ip, 80) or await self._is_port_open(ip, 443)
        except Exception:
            return False

    def export_scan_results(self, results: List[ScanResult],
                          format_type: str = "json") -> str:
        """
        Export scan results in specified format.

        Args:
            results: Scan results to export
            format_type: Export format (json, csv, xml)

        Returns:
            Formatted export string
        """
        if format_type == "json":
            return self._export_json(results)
        elif format_type == "csv":
            return self._export_csv(results)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _export_json(self, results: List[ScanResult]) -> str:
        """Export results as JSON"""
        export_data = []
        for result in results:
            export_data.append({
                "target_ip": result.target.ip_address,
                "target_hostname": result.target.hostname,
                "scan_type": result.scan_type,
                "findings": result.findings,
                "scan_duration": result.scan_duration,
                "timestamp": result.timestamp.isoformat(),
                "success": result.success,
                "error_message": result.error_message
            })

        return json.dumps(export_data, indent=2)

    def _export_csv(self, results: List[ScanResult]) -> str:
        """Export results as CSV"""
        lines = ["Target IP,Hostname,Scan Type,Findings Count,Duration,Success,Timestamp"]

        for result in results:
            findings_count = len(result.findings)
            line = ",".join([
                result.target.ip_address,
                result.target.hostname or "",
                result.scan_type,
                str(findings_count),
                ".2f",
                str(result.success),
                result.timestamp.isoformat()
            ])
            lines.append(line)

        return "\n".join(lines)

    def get_scan_statistics(self, results: List[ScanResult]) -> Dict[str, Any]:
        """Get statistics from scan results"""
        stats = {
            "total_scans": len(results),
            "successful_scans": len([r for r in results if r.success]),
            "failed_scans": len([r for r in results if not r.success]),
            "total_findings": sum(len(r.findings) for r in results),
            "scan_types": {},
            "average_duration": 0.0
        }

        # Scan type breakdown
        for result in results:
            scan_type = result.scan_type
            stats["scan_types"][scan_type] = stats["scan_types"].get(scan_type, 0) + 1

        # Average duration
        if results:
            total_duration = sum(r.scan_duration for r in results)
            stats["average_duration"] = total_duration / len(results)
