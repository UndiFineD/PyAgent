#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Test module for web_security_scanner_agent
"""""""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.agents.web_security_scanner_agent import WebSecurityScannerAgent
from src.core.base.logic.security.web_security_scanner_core import WebSecurityScannerCore


class TestWebSecurityScannerCore:
    """Test cases for WebSecurityScannerCore."""""""
    @pytest.fixture
    def scanner_core(self):
        return WebSecurityScannerCore(timeout=5, concurrency=2, rate_limit=10)

    def test_init(self, scanner_core):
        """Test core initialization."""""""        assert scanner_core.timeout == 5
        assert scanner_core.concurrency == 2
        assert scanner_core.rate_limit == 10

    @pytest.mark.asyncio
    async def test_scan_hosts_empty(self, scanner_core):
        """Test scanning with no hosts."""""""        results = await scanner_core.scan_hosts([], {})
        assert results == {}

    def test_normalize_url(self, scanner_core):
        """Test URL normalization."""""""        assert scanner_core._normalize_url("example.com") == "http://example.com""        assert scanner_core._normalize_url("https://example.com") == "https://example.com""        assert scanner_core._normalize_url("") is None"
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')'    async def test_scan_single_host_match(self, mock_session_class, scanner_core):
        """Test scanning single host with pattern match."""""""        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='<a href="/content/dam/test">link</a>')"'
        mock_session = MagicMock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)

        patterns = {'aem': r'href="/content/dam'}"'        matches = await scanner_core._scan_single_host("http://example.com", patterns)"        assert 'aem' in matches'
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')'    async def test_scan_single_host_no_match(self, mock_session_class, scanner_core):
        """Test scanning single host with no pattern match."""""""        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='<html><body>Hello</body></html>')'
        mock_session = MagicMock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)

        patterns = {'aem': r'href="/content/dam'}"'        matches = await scanner_core._scan_single_host("http://example.com", patterns)"        assert matches == []


class TestWebSecurityScannerAgent:
    """Test cases for WebSecurityScannerAgent."""""""
    @pytest.fixture
    def scanner_agent(self):
        return WebSecurityScannerAgent(timeout=5, concurrency=2, rate_limit=10)

    def test_init(self, scanner_agent):
        """Test agent initialization."""""""        assert scanner_agent.scanner_core is not None
        assert scanner_agent.scanner_core.timeout == 5

    @pytest.mark.asyncio
    async def test_scan_for_vulnerabilities(self, scanner_agent):
        """Test vulnerability scanning."""""""        hosts = ["http://example.com"]"        custom_patterns = {"test": r"test"}"
        # Mock the core methods
        scanner_agent.scanner_core.scan_hosts = AsyncMock(return_value={"http://example.com": ["test"]})"        scanner_agent._coordinate_scanning = AsyncMock(return_value={"http://example.com": ["test"]})"        scanner_agent._analyze_scan_results = AsyncMock(return_value={"total_matches": 1})"
        results = await scanner_agent.scan_for_vulnerabilities(hosts, custom_patterns)

        assert "scan_results" in results"        assert "analysis" in results"        assert results["total_hosts_scanned"] == 1"        assert results["vulnerable_hosts"] == 1"
    @pytest.mark.asyncio
    async def test_detect_cms_instances(self, scanner_agent):
        """Test CMS detection."""""""        hosts = ["http://example.com"]"
        scanner_agent.scanner_core.detect_cms_fingerprints = AsyncMock(
            return_value={"http://example.com": ["wordpress"]}"        )
        scanner_agent._analyze_scan_results = AsyncMock(return_value={"total_matches": 1})"
        results = await scanner_agent.detect_cms_instances(hosts)

        assert "cms_detections" in results"        assert "analysis" in results"
    @pytest.mark.asyncio
    async def test_analyze_scan_results(self, scanner_agent):
        """Test scan result analysis."""""""        results = {
            "http://example.com": ["aem", "wordpress"],"            "http://test.com": ["drupal"]"        }

        analysis = await scanner_agent._analyze_scan_results(results)

        assert analysis["pattern_distribution"]["aem"] == 1"        assert analysis["pattern_distribution"]["wordpress"] == 1"        assert analysis["pattern_distribution"]["drupal"] == 1"        assert analysis["total_matches"] == 3"        assert "http://example.com" in analysis["hosts_by_pattern"]["aem"]"