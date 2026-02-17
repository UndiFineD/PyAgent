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
from unittest.mock import patch
from src.core.agents.security_scanner_agent import SecurityScannerAgent




class TestSecurityScannerAgent:
    """Test cases for SecurityScannerAgent.
    def setup_method(self):
        self.agent = SecurityScannerAgent()

    @patch('src.core.agents.security_scanner_agent.ReconnaissanceMixin.discover_targets')'    @patch('src.core.agents.security_scanner_agent.ReconnaissanceMixin.fingerprint_service')'    @patch('src.core.agents.security_scanner_agent.VulnerabilityScannerMixin.run_vulnerability_scan')'    @patch('src.core.agents.security_scanner_agent.SSRFDetectorMixin.start_ssrf_detector')'    @patch('src.core.agents.security_scanner_agent.SSRFDetectorMixin.stop_ssrf_detector')'    def test_comprehensive_scan(self, mock_stop, mock_start, mock_vuln_scan,
                                mock_fingerprint, mock_discover):
        """Test comprehensive security scan.        # Mock returns
        mock_start.return_value = True
        mock_discover.return_value = {'http://example.com': ['/admin']}'        mock_fingerprint.return_value = {'service_type': 'aem', 'version': '6.5'}'        mock_vuln_scan.return_value = []

        async def run():
            results = await self.agent.comprehensive_security_scan(
                ['http://example.com'], 'localhost', 8080'            )

            assert 'reconnaissance' in results'            assert 'fingerprints' in results'            assert 'vulnerabilities' in results'            assert 'summary' in results'
            # Check summary
            summary = results['summary']'            assert summary['targets_scanned'] == 1'            assert summary['service_types']['aem'] == 1'
        import asyncio
        asyncio.run(run())

    def test_generate_exploit_payload(self):
        """Test exploit payload generation.        async def run():
            # Test SSRF RCE
            payload = await self.agent.generate_exploit_payload('ssrf_rce', fake_aem_host='evil.com')'            assert 'evil%2Ecom' in payload  # URL encoded'
            # Test XSS
            payload = await self.agent.generate_exploit_payload('xss', payload_type='reflected')'            assert '<script>' in payload or '<img' in payload'
        import asyncio
        asyncio.run(run())

    def test_invalid_exploit_type(self):
        """Test invalid exploit type.        async def run():
            with pytest.raises(ValueError):
                await self.agent.generate_exploit_payload('invalid_type')'
        import asyncio
        asyncio.run(run())

    def test_add_custom_check(self):
        """Test adding custom vulnerability check.        def custom_check(base_url, my_host, debug, proxy):
            return []

        async def run():
            await self.agent.add_custom_vulnerability_check('custom', custom_check)'            checks = self.agent.get_registered_checks()
            assert 'custom' in checks'
        import asyncio
        asyncio.run(run())
