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

# Acunetix Automation Core - Web Vulnerability Scanning Automation
# Based on patterns from AcuAutomate repository

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import aiohttp
import re


class ScanType(Enum):
    """Acunetix scan types"""
    FULL = "full"
    HIGH = "high"
    WEAK = "weak"
    CRAWL = "crawl"
    XSS = "xss"
    SQL = "sql"


class ScanStatus(Enum):
    """Scan status enumeration"""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"
    SCHEDULED = "scheduled"


@dataclass
class ScanTarget:
    """Represents a target for scanning"""
    url: str
    description: Optional[str] = None
    criticality: int = 10
    target_id: Optional[str] = None
    scan_id: Optional[str] = None
    status: ScanStatus = ScanStatus.SCHEDULED
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class ScanResult:
    """Result from a vulnerability scan"""
    scan_id: str
    target_url: str
    scan_type: ScanType
    status: ScanStatus
    vulnerabilities_found: int = 0
    high_severity: int = 0
    medium_severity: int = 0
    low_severity: int = 0
    info_severity: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    report_url: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AcunetixConfig:
    """Configuration for Acunetix API"""
    url: str
    port: int
    api_key: str
    timeout: int = 30
    verify_ssl: bool = False

    @property
    def base_url(self) -> str:
        return f"{self.url}:{self.port}"


class AcunetixAutomationCore:
    """
    Acunetix Automation Core for automated web vulnerability scanning.

    Provides capabilities for automated scanning, batch processing,
    scan management, and integration with Acunetix vulnerability scanner.
    """

    # Acunetix scan profile IDs
    SCAN_PROFILES = {
        ScanType.FULL: "11111111-1111-1111-1111-111111111111",
        ScanType.HIGH: "11111111-1111-1111-1111-111111111112",
        ScanType.WEAK: "11111111-1111-1111-1111-111111111115",
        ScanType.CRAWL: "11111111-1111-1111-1111-111111111117",
        ScanType.XSS: "11111111-1111-1111-1111-111111111116",
        ScanType.SQL: "11111111-1111-1111-1111-111111111113",
    }

    def __init__(self, config: Optional[AcunetixConfig] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.active_scans: Dict[str, ScanTarget] = {}
        self.scan_history: List[ScanResult] = []
        self.targets: Dict[str, ScanTarget] = {}

    def _is_valid_url(self, url: str) -> bool:
        """Simple URL validation"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url_pattern.match(url) is not None

    async def initialize(self, config_path: Optional[str] = None) -> bool:
        """Initialize the Acunetix automation core"""
        try:
            if not self.config and config_path:
                self.config = await self.load_config(config_path)

            if not self.config:
                self.logger.error("No configuration provided for Acunetix automation")
                return False

            # Create aiohttp session
            self.session = aiohttp.ClientSession(
                headers={
                    "X-Auth": self.config.api_key,
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )

            # Test connection
            await self.test_connection()

            self.logger.info("Acunetix Automation Core initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Acunetix Automation Core: {e}")
            return False

    async def load_config(self, config_path: str) -> AcunetixConfig:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            return AcunetixConfig(
                url=config_data['url'],
                port=config_data['port'],
                api_key=config_data['api_key']
            )
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_path}: {e}")

    async def test_connection(self) -> bool:
        """Test connection to Acunetix API"""
        if not self.session:
            return False

        try:
            url = f"{self.config.base_url}/api/v1/scans"
            async with self.session.get(url) as response:
                return response.status == 200
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False

    async def add_target(self, url: str, description: Optional[str] = None, criticality: int = 10) -> Optional[str]:
        """
        Add a target to Acunetix for scanning

        Args:
            url: Target URL to scan
            description: Description of the target
            criticality: Criticality level (1-10)

        Returns:
            Target ID if successful, None otherwise
        """
        if not self._is_valid_url(url):
            self.logger.error(f"Invalid URL: {url}")
            return None

        try:
            target_data = {
                "address": url,
                "description": description or url,
                "criticality": str(criticality)
            }

            url_endpoint = f"{self.config.base_url}/api/v1/targets"
            async with self.session.post(url_endpoint, json=target_data) as response:
                if response.status == 201:
                    result = await response.json()
                    target_id = result['target_id']

                    # Store target locally
                    target = ScanTarget(
                        url=url,
                        description=description,
                        criticality=criticality,
                        target_id=target_id
                    )
                    self.targets[target_id] = target

                    self.logger.info(f"Added target: {url} (ID: {target_id})")
                    return target_id
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to add target {url}: {response.status} - {error_text}")
                    return None

        except Exception as e:
            self.logger.error(f"Error adding target {url}: {e}")
            return None

    async def start_scan(
        self,
        target_id: str,
        scan_type: ScanType = ScanType.FULL,
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        Start a vulnerability scan on a target

        Args:
            target_id: Target ID to scan
            scan_type: Type of scan to perform
            description: Scan description

        Returns:
            Scan ID if successful, None otherwise
        """
        if target_id not in self.targets:
            self.logger.error(f"Target {target_id} not found")
            return None

        try:
            profile_id = self.SCAN_PROFILES[scan_type]

            scan_data = {
                "target_id": target_id,
                "profile_id": profile_id,
                "schedule": {
                    "disable": False,
                    "start_date": None,
                    "time_sensitive": False
                }
            }

            if description:
                scan_data["description"] = description

            url_endpoint = f"{self.config.base_url}/api/v1/scans"
            async with self.session.post(url_endpoint, json=scan_data) as response:
                if response.status == 201:
                    result = await response.json()
                    scan_id = result['scan_id']

                    # Update target with scan info
                    self.targets[target_id].scan_id = scan_id
                    self.targets[target_id].status = ScanStatus.PROCESSING
                    self.active_scans[scan_id] = self.targets[target_id]

                    self.logger.info(f"Started {scan_type.value} scan on {self.targets[target_id].url} (Scan ID: {scan_id})")
                    return scan_id
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to start scan: {response.status} - {error_text}")
                    return None

        except Exception as e:
            self.logger.error(f"Error starting scan: {e}")
            return None

    async def scan_url(
        self,
        url: str,
        scan_type: ScanType = ScanType.FULL,
        description: Optional[str] = None,
        criticality: int = 10
    ) -> Optional[str]:
        """
        Convenience method to add target and start scan in one call

        Args:
            url: URL to scan
            scan_type: Type of scan to perform
            description: Scan description
            criticality: Target criticality

        Returns:
            Scan ID if successful, None otherwise
        """
        target_id = await self.add_target(url, description, criticality)
        if target_id:
            return await self.start_scan(target_id, scan_type, description)
        return None

    async def scan_from_file(
        self,
        file_path: str,
        scan_type: ScanType = ScanType.FULL,
        description: Optional[str] = None
    ) -> List[str]:
        """
        Scan multiple targets from a file

        Args:
            file_path: Path to file containing URLs (one per line)
            scan_type: Type of scan to perform
            description: Scan description

        Returns:
            List of scan IDs
        """
        scan_ids = []

        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]

            for url in urls:
                if self._is_valid_url(url):
                    scan_id = await self.scan_url(url, scan_type, description)
                    if scan_id:
                        scan_ids.append(scan_id)
                else:
                    self.logger.warning(f"Skipping invalid URL: {url}")

        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")

        self.logger.info(f"Started {len(scan_ids)} scans from file {file_path}")
        return scan_ids

    async def scan_from_pipeline(
        self,
        urls: List[str],
        scan_type: ScanType = ScanType.FULL,
        description: Optional[str] = None
    ) -> List[str]:
        """
        Scan multiple targets from pipeline input

        Args:
            urls: List of URLs to scan
            scan_type: Type of scan to perform
            description: Scan description

        Returns:
            List of scan IDs
        """
        scan_ids = []

        for url in urls:
            url = url.strip()
            if url and self._is_valid_url(url):
                scan_id = await self.scan_url(url, scan_type, description)
                if scan_id:
                    scan_ids.append(scan_id)
            else:
                self.logger.warning(f"Skipping invalid URL: {url}")

        self.logger.info(f"Started {len(scan_ids)} scans from pipeline")
        return scan_ids

    async def stop_scan(self, scan_id: str) -> bool:
        """
        Stop a running scan

        Args:
            scan_id: Scan ID to stop

        Returns:
            True if successful, False otherwise
        """
        try:
            url_endpoint = f"{self.config.base_url}/api/v1/scans/{scan_id}/abort"
            async with self.session.post(url_endpoint) as response:
                if response.status == 204:
                    if scan_id in self.active_scans:
                        self.active_scans[scan_id].status = ScanStatus.ABORTED
                        self.active_scans[scan_id].completed_at = datetime.now()
                    self.logger.info(f"Stopped scan: {scan_id}")
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to stop scan {scan_id}: {response.status} - {error_text}")
                    return False

        except Exception as e:
            self.logger.error(f"Error stopping scan {scan_id}: {e}")
            return False

    async def stop_all_scans(self) -> int:
        """
        Stop all running scans

        Returns:
            Number of scans stopped
        """
        try:
            # Get all processing scans
            url_endpoint = f"{self.config.base_url}/api/v1/scans?q=status:processing;"
            async with self.session.get(url_endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    scans = data.get("scans", [])

                    stopped_count = 0
                    for scan in scans:
                        scan_id = scan["scan_id"]
                        if await self.stop_scan(scan_id):
                            stopped_count += 1

                    self.logger.info(f"Stopped {stopped_count} scans")
                    return stopped_count
                else:
                    self.logger.error(f"Failed to get running scans: {response.status}")
                    return 0

        except Exception as e:
            self.logger.error(f"Error stopping all scans: {e}")
            return 0

    async def get_scan_status(self, scan_id: str) -> Optional[ScanStatus]:
        """
        Get the status of a scan

        Args:
            scan_id: Scan ID to check

        Returns:
            Scan status if found, None otherwise
        """
        try:
            url_endpoint = f"{self.config.base_url}/api/v1/scans/{scan_id}"
            async with self.session.get(url_endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    status_str = data.get("status", "").lower()
                    try:
                        status = ScanStatus(status_str)
                        # Update local status
                        if scan_id in self.active_scans:
                            self.active_scans[scan_id].status = status
                            if status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.ABORTED]:
                                self.active_scans[scan_id].completed_at = datetime.now()
                        return status
                    except ValueError:
                        self.logger.warning(f"Unknown scan status: {status_str}")
                        return None
                else:
                    self.logger.error(f"Failed to get scan status: {response.status}")
                    return None

        except Exception as e:
            self.logger.error(f"Error getting scan status: {e}")
            return None

    async def get_scan_results(self, scan_id: str) -> Optional[ScanResult]:
        """
        Get detailed results for a completed scan

        Args:
            scan_id: Scan ID to get results for

        Returns:
            Scan result details if available
        """
        try:
            url_endpoint = f"{self.config.base_url}/api/v1/scans/{scan_id}/results"
            async with self.session.get(url_endpoint) as response:
                if response.status == 200:
                    data = await response.json()

                    # Create scan result
                    result = ScanResult(
                        scan_id=scan_id,
                        target_url=self.active_scans.get(scan_id, ScanTarget("unknown")).url,
                        scan_type=ScanType.FULL,  # Would need to track this
                        status=ScanStatus.COMPLETED,
                        vulnerabilities_found=data.get("vulnerabilities_count", 0),
                        high_severity=data.get("high_severity_count", 0),
                        medium_severity=data.get("medium_severity_count", 0),
                        low_severity=data.get("low_severity_count", 0),
                        info_severity=data.get("info_severity_count", 0),
                        details=data
                    )

                    self.scan_history.append(result)
                    return result
                else:
                    self.logger.error(f"Failed to get scan results: {response.status}")
                    return None

        except Exception as e:
            self.logger.error(f"Error getting scan results: {e}")
            return None

    async def list_scans(self, status_filter: Optional[ScanStatus] = None) -> List[Dict[str, Any]]:
        """
        List scans with optional status filter

        Args:
            status_filter: Filter scans by status

        Returns:
            List of scan information
        """
        try:
            query = f"q=status:{status_filter.value};" if status_filter else ""
            url_endpoint = f"{self.config.base_url}/api/v1/scans{query}"

            async with self.session.get(url_endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("scans", [])
                else:
                    self.logger.error(f"Failed to list scans: {response.status}")
                    return []

        except Exception as e:
            self.logger.error(f"Error listing scans: {e}")
            return []

    async def get_scan_summary(self) -> Dict[str, Any]:
        """Get summary of all scans and their status"""
        summary = {
            "total_scans": len(self.scan_history),
            "active_scans": len(self.active_scans),
            "completed_scans": 0,
            "failed_scans": 0,
            "aborted_scans": 0,
            "total_vulnerabilities": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "scan_types": {},
            "recent_scans": []
        }

        # Count by status
        for scan in self.active_scans.values():
            if scan.status == ScanStatus.COMPLETED:
                summary["completed_scans"] += 1
            elif scan.status == ScanStatus.FAILED:
                summary["failed_scans"] += 1
            elif scan.status == ScanStatus.ABORTED:
                summary["aborted_scans"] += 1

        # Aggregate vulnerability counts
        for result in self.scan_history:
            summary["total_vulnerabilities"] += result.vulnerabilities_found
            summary["high_severity"] += result.high_severity
            summary["medium_severity"] += result.medium_severity
            summary["low_severity"] += result.low_severity

            # Count scan types
            scan_type = result.scan_type.value
            summary["scan_types"][scan_type] = summary["scan_types"].get(scan_type, 0) + 1

        # Recent scans
        recent = sorted(self.scan_history[-5:], key=lambda x: x.start_time, reverse=True)
        summary["recent_scans"] = [
            {
                "scan_id": r.scan_id,
                "target": r.target_url,
                "type": r.scan_type.value,
                "status": r.status.value,
                "vulnerabilities": r.vulnerabilities_found,
                "start_time": r.start_time.isoformat()
            }
            for r in recent
        ]

        return summary

    async def export_scan_report(
        self,
        scan_id: str,
        format: str = "json",
        filepath: Optional[str] = None
    ) -> Optional[str]:
        """
        Export scan results to file

        Args:
            scan_id: Scan ID to export
            format: Export format (json, xml, html)
            filepath: Output file path

        Returns:
            File path if successful, None otherwise
        """
        try:
            result = await self.get_scan_results(scan_id)
            if not result:
                return None

            if not filepath:
                filepath = f"scan_report_{scan_id}.{format}"

            if format == "json":
                with open(filepath, 'w') as f:
                    json.dump(result.details, f, indent=2, default=str)
            else:
                # For other formats, just save the raw response
                with open(filepath, 'w') as f:
                    json.dump(result.details, f, indent=2, default=str)

            self.logger.info(f"Exported scan report to {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error exporting scan report: {e}")
            return None

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self.session:
            await self.session.close()

        self.active_scans.clear()
        self.targets.clear()
        self.logger.info("Acunetix Automation Core cleaned up")