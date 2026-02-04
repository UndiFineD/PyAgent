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
AEM Detection Core

This core implements AEM (Adobe Experience Manager) detection patterns inspired by aem-eye.
It provides fast, concurrent detection of AEM installations through signature-based analysis.

Key Features:
- Fast concurrent AEM detection using async HTTP requests
- Signature-based detection with configurable patterns
- Rate limiting and concurrency controls
- Support for large-scale host scanning
- AEM-specific path and content detection
- Version fingerprinting capabilities
- Integration with vulnerability assessment workflows
"""

import asyncio
import json
import logging
import re
import aiohttp
import ssl
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from concurrent.futures import ThreadPoolExecutor
import time
import os

from src.core.base.common.base_core import BaseCore
from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.state.agent_state_manager import StateTransaction

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AEMDetectionResult:
    """Result of AEM detection for a single host."""
    host: str
    detected: bool
    confidence: float  # 0.0 to 1.0
    matched_patterns: List[str]
    response_time: float
    status_code: Optional[int]
    server_header: Optional[str]
    aem_version: Optional[str]
    detected_paths: List[str]
    vulnerabilities: List[Dict[str, Any]]
    scan_timestamp: datetime


@dataclass
class AEMScanConfig:
    """Configuration for AEM detection scan."""
    concurrency: int = 100
    rate_limit: int = 1000  # requests per second
    timeout: int = 10  # seconds
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    follow_redirects: bool = True
    max_redirects: int = 10
    verify_ssl: bool = False
    patterns: Dict[str, str] = field(default_factory=lambda: {
        "content_dam": r'href="\/content\/dam[^"]*"',
        "clientlibs": r'href="\/etc\/clientlibs[^"]*"',
        "aem_start": r'href="\/libs\/granite[^"]*"',
        "dispatcher": r'href="\/content\/[^"]*\.html"',
        "crx_de": r'href="\/crx\/de[^"]*"',
        "system_console": r'href="\/system\/console[^"]*"',
        " geometrixx": r'geometrixx',  # Default demo site
        "we_retail": r'we-retail',  # Default demo site
    })


@dataclass
class AEMScanResults:
    """Results of a complete AEM detection scan."""
    total_hosts: int
    detected_hosts: int
    scan_duration: float
    results: List[AEMDetectionResult]
    config: AEMScanConfig
    scan_timestamp: datetime


class AEMDetectionCore(BaseCore):
    """
    Core for AEM (Adobe Experience Manager) detection and analysis.

    This core provides fast, concurrent detection of AEM installations using
    signature-based analysis patterns inspired by the aem-eye tool.
    """

    def __init__(self):
        super().__init__()
        self.name = "AEMDetectionCore"
        self.version = "1.0.0"
        self.description = "Fast AEM Detection and Analysis"

        # Default scan configuration
        self.default_config = AEMScanConfig()

        # Known AEM versions and their signatures
        self.aem_versions = {
            "6.5": ["6.5", "granite:6.5"],
            "6.4": ["6.4", "granite:6.4"],
            "6.3": ["6.3", "granite:6.3"],
            "6.2": ["6.2", "granite:6.2"],
            "6.1": ["6.1", "granite:6.1"],
            "6.0": ["6.0", "granite:6.0"],
            "5.6": ["5.6", "cq:5.6"],
        }

        # Known AEM vulnerabilities by version
        self.known_vulnerabilities = {
            "6.5": [
                {"cve": "CVE-2023-22275", "severity": "Critical", "description": "RCE via Asset Upload"},
                {"cve": "CVE-2023-22276", "severity": "High", "description": "Privilege Escalation"},
            ],
            "6.4": [
                {"cve": "CVE-2022-25287", "severity": "High", "description": "Deserialization RCE"},
                {"cve": "CVE-2021-27648", "severity": "Medium", "description": "Information Disclosure"},
            ],
            "6.3": [
                {"cve": "CVE-2020-8840", "severity": "Critical", "description": "RCE via DAVEx"},
            ],
        }

    async def detect_aem_single(self, host: str, config: Optional[AEMScanConfig] = None) -> AEMDetectionResult:
        """
        Detect AEM on a single host.

        Args:
            host: Target host URL
            config: Scan configuration

        Returns:
            AEMDetectionResult: Detection result for the host
        """
        if config is None:
            config = self.default_config

        start_time = time.time()

        try:
            # Create SSL context
            ssl_context = ssl.create_default_context()
            if not config.verify_ssl:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

            # Create connector with timeout
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=1,
                limit_per_host=1,
                ttl_dns_cache=30
            )

            # Create session with custom headers
            headers = {
                'User-Agent': config.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close'
            }

            timeout = aiohttp.ClientTimeout(total=config.timeout)

            async with aiohttp.ClientSession(
                connector=connector,
                headers=headers,
                timeout=timeout,
                max_redirects=config.max_redirects if config.follow_redirects else 0
            ) as session:

                try:
                    async with session.get(host) as response:
                        response_time = time.time() - start_time
                        status_code = response.status
                        server_header = response.headers.get('Server', '')
                        content_type = response.headers.get('Content-Type', '')

                        # Only check HTML content
                        if 'text/html' not in content_type.lower():
                            return AEMDetectionResult(
                                host=host,
                                detected=False,
                                confidence=0.0,
                                matched_patterns=[],
                                response_time=response_time,
                                status_code=status_code,
                                server_header=server_header,
                                aem_version=None,
                                detected_paths=[],
                                vulnerabilities=[],
                                scan_timestamp=datetime.now()
                            )

                        # Read response body
                        body = await response.text()

                        # Check for AEM patterns
                        matched_patterns = []
                        detected_paths = []
                        confidence = 0.0

                        for pattern_name, pattern in config.patterns.items():
                            try:
                                if re.search(pattern, body, re.IGNORECASE):
                                    matched_patterns.append(pattern_name)
                                    confidence += 0.2  # Each pattern match increases confidence

                                    # Extract actual paths for some patterns
                                    if pattern_name in ['content_dam', 'clientlibs', 'aem_start']:
                                        matches = re.findall(pattern, body, re.IGNORECASE)
                                        detected_paths.extend(matches[:5])  # Limit to 5 matches

                            except re.error as e:
                                logger.warning(f"Invalid regex pattern {pattern_name}: {e}")
                                continue

                        # Cap confidence at 1.0
                        confidence = min(confidence, 1.0)

                        # Determine if AEM is detected (require at least 2 pattern matches or high confidence)
                        detected = len(matched_patterns) >= 2 or confidence >= 0.6

                        # Try to detect AEM version
                        aem_version = self._detect_aem_version(body)

                        # Get relevant vulnerabilities
                        vulnerabilities = []
                        if aem_version and aem_version in self.known_vulnerabilities:
                            vulnerabilities = self.known_vulnerabilities[aem_version]

                        return AEMDetectionResult(
                            host=host,
                            detected=detected,
                            confidence=confidence,
                            matched_patterns=matched_patterns,
                            response_time=response_time,
                            status_code=status_code,
                            server_header=server_header,
                            aem_version=aem_version,
                            detected_paths=detected_paths,
                            vulnerabilities=vulnerabilities,
                            scan_timestamp=datetime.now()
                        )

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    response_time = time.time() - start_time
                    logger.debug(f"Request failed for {host}: {e}")
                    return AEMDetectionResult(
                        host=host,
                        detected=False,
                        confidence=0.0,
                        matched_patterns=[],
                        response_time=response_time,
                        status_code=None,
                        server_header=None,
                        aem_version=None,
                        detected_paths=[],
                        vulnerabilities=[],
                        scan_timestamp=datetime.now()
                    )

        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Error scanning {host}: {e}")
            return AEMDetectionResult(
                host=host,
                detected=False,
                confidence=0.0,
                matched_patterns=[],
                response_time=response_time,
                status_code=None,
                server_header=None,
                aem_version=None,
                detected_paths=[],
                vulnerabilities=[],
                scan_timestamp=datetime.now()
            )

    async def detect_aem_batch(self, hosts: List[str], config: Optional[AEMScanConfig] = None) -> AEMScanResults:
        """
        Detect AEM on multiple hosts concurrently.

        Args:
            hosts: List of target host URLs
            config: Scan configuration

        Returns:
            AEMScanResults: Complete scan results
        """
        if config is None:
            config = self.default_config

        start_time = time.time()

        # Create semaphore for rate limiting
        semaphore = asyncio.Semaphore(config.concurrency)

        async def scan_with_semaphore(host: str):
            async with semaphore:
                # Simple rate limiting delay
                await asyncio.sleep(1.0 / config.rate_limit)
                return await self.detect_aem_single(host, config)

        # Create tasks for all hosts
        tasks = [scan_with_semaphore(host) for host in hosts]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error scanning {hosts[i]}: {result}")
                # Create error result
                processed_results.append(AEMDetectionResult(
                    host=hosts[i],
                    detected=False,
                    confidence=0.0,
                    matched_patterns=[],
                    response_time=0.0,
                    status_code=None,
                    server_header=None,
                    aem_version=None,
                    detected_paths=[],
                    vulnerabilities=[],
                    scan_timestamp=datetime.now()
                ))
            else:
                processed_results.append(result)

        # Calculate statistics
        detected_hosts = sum(1 for r in processed_results if r.detected)
        scan_duration = time.time() - start_time

        return AEMScanResults(
            total_hosts=len(hosts),
            detected_hosts=detected_hosts,
            scan_duration=scan_duration,
            results=processed_results,
            config=config,
            scan_timestamp=datetime.now()
        )

    def _detect_aem_version(self, body: str) -> Optional[str]:
        """
        Attempt to detect AEM version from response body.

        Args:
            body: HTML response body

        Returns:
            Optional[str]: Detected AEM version or None
        """
        for version, signatures in self.aem_versions.items():
            for signature in signatures:
                if signature in body:
                    return version

        # Try to extract version from meta tags or scripts
        version_patterns = [
            r'granite:([0-9]+\.[0-9]+)',
            r'cq:([0-9]+\.[0-9]+)',
            r'AEM\s+([0-9]+\.[0-9]+)',
            r'Adobe\s+Experience\s+Manager\s+([0-9]+\.[0-9]+)'
        ]

        for pattern in version_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    async def load_hosts_from_file(self, file_path: str) -> List[str]:
        """
        Load hosts from a file.

        Args:
            file_path: Path to file containing hosts (one per line)

        Returns:
            List[str]: List of hosts
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                hosts = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            # Ensure hosts have http/https prefix
            processed_hosts = []
            for host in hosts:
                if not host.startswith(('http://', 'https://')):
                    # Try both http and https
                    processed_hosts.append(f"http://{host}")
                    processed_hosts.append(f"https://{host}")
                else:
                    processed_hosts.append(host)

            return processed_hosts

        except Exception as e:
            logger.error(f"Failed to load hosts from file {file_path}: {e}")
            return []

    async def export_results(self, results: AEMScanResults, output_file: str, format: str = 'json') -> bool:
        """
        Export scan results to a file.

        Args:
            results: Scan results to export
            output_file: Output file path
            format: Export format ('json' or 'csv')

        Returns:
            bool: True if export successful
        """
        try:
            if format.lower() == 'json':
                # Convert results to dict
                results_dict = {
                    'total_hosts': results.total_hosts,
                    'detected_hosts': results.detected_hosts,
                    'scan_duration': results.scan_duration,
                    'scan_timestamp': results.scan_timestamp.isoformat(),
                    'config': {
                        'concurrency': results.config.concurrency,
                        'rate_limit': results.config.rate_limit,
                        'timeout': results.config.timeout
                    },
                    'results': [
                        {
                            'host': r.host,
                            'detected': r.detected,
                            'confidence': r.confidence,
                            'matched_patterns': r.matched_patterns,
                            'response_time': r.response_time,
                            'status_code': r.status_code,
                            'server_header': r.server_header,
                            'aem_version': r.aem_version,
                            'detected_paths': r.detected_paths,
                            'vulnerabilities': r.vulnerabilities,
                            'scan_timestamp': r.scan_timestamp.isoformat()
                        }
                        for r in results.results
                    ]
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results_dict, f, indent=2, ensure_ascii=False)

            elif format.lower() == 'csv':
                import csv

                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Host', 'Detected', 'Confidence', 'Matched_Patterns',
                        'Response_Time', 'Status_Code', 'Server_Header',
                        'AEM_Version', 'Vulnerabilities_Count'
                    ])

                    for result in results.results:
                        writer.writerow([
                            result.host,
                            result.detected,
                            f"{result.confidence:.2f}",
                            ';'.join(result.matched_patterns),
                            f"{result.response_time:.2f}",
                            result.status_code or '',
                            result.server_header or '',
                            result.aem_version or '',
                            len(result.vulnerabilities)
                        ])

            else:
                logger.error(f"Unsupported export format: {format}")
                return False

            logger.info(f"Results exported to {output_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to export results: {e}")
            return False

    async def execute_task(self, context: CascadeContext) -> Dict[str, Any]:
        """
        Execute AEM detection task.

        Args:
            context: Cascade context containing task parameters

        Returns:
            Dict containing detection results
        """
        try:
            task_type = context.task.get('type', 'single_scan')

            if task_type == 'single_scan':
                host = context.task.get('host', '')
                if not host:
                    raise ValueError("Host is required for single scan")

                config = self._parse_config(context.task.get('config', {}))
                result = await self.detect_aem_single(host, config)

                return {
                    'host': result.host,
                    'detected': result.detected,
                    'confidence': result.confidence,
                    'matched_patterns': result.matched_patterns,
                    'response_time': result.response_time,
                    'status_code': result.status_code,
                    'server_header': result.server_header,
                    'aem_version': result.aem_version,
                    'detected_paths': result.detected_paths,
                    'vulnerabilities': result.vulnerabilities
                }

            elif task_type == 'batch_scan':
                hosts_file = context.task.get('hosts_file', '')
                if not hosts_file:
                    raise ValueError("Hosts file is required for batch scan")

                hosts = await self.load_hosts_from_file(hosts_file)
                if not hosts:
                    raise ValueError(f"No valid hosts found in {hosts_file}")

                config = self._parse_config(context.task.get('config', {}))
                results = await self.detect_aem_batch(hosts, config)

                # Export results if requested
                output_file = context.task.get('output_file')
                if output_file:
                    export_format = context.task.get('export_format', 'json')
                    await self.export_results(results, output_file, export_format)

                return {
                    'total_hosts': results.total_hosts,
                    'detected_hosts': results.detected_hosts,
                    'scan_duration': results.scan_duration,
                    'detection_rate': results.detected_hosts / results.total_hosts if results.total_hosts > 0 else 0,
                    'results_summary': [
                        {
                            'host': r.host,
                            'detected': r.detected,
                            'confidence': r.confidence,
                            'aem_version': r.aem_version,
                            'vulnerabilities_count': len(r.vulnerabilities)
                        }
                        for r in results.results if r.detected
                    ]
                }

            else:
                raise ValueError(f"Unknown task type: {task_type}")

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            raise

    def _parse_config(self, config_dict: Dict[str, Any]) -> AEMScanConfig:
        """Parse configuration from task parameters."""
        config = AEMScanConfig()

        if 'concurrency' in config_dict:
            config.concurrency = int(config_dict['concurrency'])
        if 'rate_limit' in config_dict:
            config.rate_limit = int(config_dict['rate_limit'])
        if 'timeout' in config_dict:
            config.timeout = int(config_dict['timeout'])
        if 'user_agent' in config_dict:
            config.user_agent = str(config_dict['user_agent'])
        if 'follow_redirects' in config_dict:
            config.follow_redirects = bool(config_dict['follow_redirects'])
        if 'max_redirects' in config_dict:
            config.max_redirects = int(config_dict['max_redirects'])
        if 'verify_ssl' in config_dict:
            config.verify_ssl = bool(config_dict['verify_ssl'])

        return config

    async def validate_task(self, context: CascadeContext) -> bool:
        """
        Validate AEM detection task.

        Args:
            context: Cascade context containing task parameters

        Returns:
            bool: True if task is valid
        """
        required_fields = ['type']
        task_data = context.task

        for field in required_fields:
            if field not in task_data:
                return False

        valid_types = ['single_scan', 'batch_scan']

        if task_data['type'] not in valid_types:
            return False

        if task_data['type'] == 'single_scan':
            return 'host' in task_data
        elif task_data['type'] == 'batch_scan':
            return 'hosts_file' in task_data

        return True

    def get_capabilities(self) -> List[str]:
        """Get core capabilities."""
        return [
            'aem_detection',
            'cms_fingerprinting',
            'vulnerability_scanning',
            'web_reconnaissance',
            'content_discovery'
        ]

    def get_supported_task_types(self) -> List[str]:
        """Get supported task types."""
        return [
            'single_scan',
            'batch_scan'
        ]