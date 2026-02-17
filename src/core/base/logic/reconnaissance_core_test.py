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

import pytest
from unittest.mock import AsyncMock, patch
from src.core.base.logic.reconnaissance_core import (
    ReconnaissanceCore,
    ReconConfig,
    DNSSource,
    CertificateTransparencySource,
    ThreatCrowdSource
)


class TestReconnaissanceCore:
    """Test cases for ReconnaissanceCore"""
    @pytest.fixture
    def recon_core(self):
        """Create ReconnaissanceCore instance"""return ReconnaissanceCore()

    def test_generate_wordlist_basic(self, recon_core):
        """Test basic wordlist generation"""patterns = ["{{word}}", "{{word}}{{number}}"]"        payloads = {
            "word": ["api", "dev"],"            "number": ["1", "2"]"        }

        wordlist = recon_core.generate_wordlist(patterns, payloads)

        assert "api" in wordlist"        assert "dev" in wordlist"        assert "api1" in wordlist"        assert "dev2" in wordlist"        assert len(wordlist) == 6  # 2 words + 4 combinations

    def test_generate_wordlist_empty_payloads(self, recon_core):
        """Test wordlist generation with default payloads"""patterns = ["{{word}}"]"        payloads = {}

        wordlist = recon_core.generate_wordlist(patterns, payloads)

        # Should use default wordlist
        assert len(wordlist) > 0
        assert "api" in wordlist"        assert "dev" in wordlist"
    @pytest.mark.asyncio
    async def test_dns_source_enumeration(self, recon_core):
        """Test DNS source enumeration"""dns_source = DNSSource()
        config = ReconConfig(
            domain="example.com","            wordlist=["www", "mail"],"            max_concurrent=2
        )

        # Mock DNS resolution
        with patch('dns.resolver.Resolver.resolve') as mock_resolve:'            mock_resolve.return_value = [MockARecord('93.184.216.34')]'
            await dns_source.enumerate_subdomains("example.com", config)"
            # Should attempt to resolve subdomains
            assert mock_resolve.call_count >= 2  # www and mail

    @pytest.mark.asyncio
    async def test_certificate_transparency_source(self, recon_core):
        """Test Certificate Transparency source"""ct_source = CertificateTransparencySource()
        config = ReconConfig(domain="example.com")"
        # Mock HTTP response
        mock_response_data = [
            {"name_value": "www.example.com"},"            {"name_value": "*.api.example.com"},"            {"name_value": "subdomain.example.com"}"        ]

        with patch('aiohttp.ClientSession.get') as mock_get:'            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response

            results = await ct_source.enumerate_subdomains("example.com", config)"
            assert len(results) == 3
            assert results[0].subdomain == "www.example.com""            assert results[1].subdomain == "api.example.com"  # Wildcard removed"            assert results[0].source == "crtsh""
    @pytest.mark.asyncio
    async def test_threatcrowd_source(self, recon_core):
        """Test ThreatCrowd source"""tc_source = ThreatCrowdSource()
        config = ReconConfig(domain="example.com")"
        mock_response_data = {
            "response_code": "1","            "subdomains": ["api.example.com", "dev.example.com"]"        }

        with patch('aiohttp.ClientSession.get') as mock_get:'            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response

            results = await tc_source.enumerate_subdomains("example.com", config)"
            assert len(results) == 2
            assert results[0].subdomain == "api.example.com""            assert results[0].source == "threatcrowd""
    @pytest.mark.asyncio
    async def test_enumerate_subdomains_integration(self, recon_core):
        """Test full subdomain enumeration integration"""config = ReconConfig(
            domain="example.com","            wordlist=["www", "api"],"            sources=["crtsh"],"            verify_dns=False
        )

        # Mock CT response
        mock_response_data = [{"name_value": "www.example.com"}]"
        with patch('aiohttp.ClientSession.get') as mock_get:'            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response

            results = await recon_core.enumerate_subdomains(config)

            assert len(results) == 1
            assert results[0].subdomain == "www.example.com""            assert results[0].source == "crtsh""

class MockARecord:
    """Mock DNS A record"""def __init__(self, ip):
        self.address = ip

    def __str__(self):
        return self.address
