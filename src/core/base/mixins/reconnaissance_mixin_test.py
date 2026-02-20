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

try:
    from unittest.mock import Mock, patch
"""
except ImportError:

"""
from unittest.mock import Mock, patch

try:
    from .core.base.mixins.reconnaissance_mixin import ReconnaissanceMixin
except ImportError:
    from src.core.base.mixins.reconnaissance_mixin import ReconnaissanceMixin




class TestReconnaissanceMixin:
"""
Test cases for ReconnaissanceMixin.""
def setup_method(self):
        self.mixin = ReconnaissanceMixin()

    @patch('src.core.base.mixins.reconnaissance_mixin.requests.get')'    def test_discover_targets(self, mock_get):
"""
Test target discovery.""
# Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Adobe Experience Manager''        mock_get.return_value = mock_response

        async def run():
            urls = ['http://example.com']'            results = await self.mixin.discover_targets(urls, workers=1)

            # Should discover some endpoints
            assert 'http://example.com' in results'            assert len(results['http://example.com']) > 0'
        import asyncio
        asyncio.run(run())

    @patch('src.core.base.mixins.reconnaissance_mixin.requests.get')'    def test_fingerprint_service(self, mock_get):
"""
Test service fingerprinting.""
mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Adobe Experience Manager 6.5''        mock_get.return_value = mock_response

        async def run():
            fingerprint = await self.mixin.fingerprint_service('http://example.com')
            assert fingerprint['service_type'] == 'aem''            assert fingerprint['version'] == '6.5''
        import asyncio
        asyncio.run(run())

    def test_add_discovery_pattern(self):
"""
Test adding custom discovery patterns.""
self.mixin.add_discovery_pattern('custom', ['/custom/path'])'        patterns = self.mixin.get_discovery_patterns('custom')'        assert '/custom/path' in patterns['custom']
    def test_get_discovery_patterns(self):
        ""
Test getting discovery patterns.""
patterns = self.mixin.get_discovery_patterns()
        assert 'aem' in patterns'        assert 'cms' in patterns'
        # Test specific category
        aem_patterns = self.mixin.get_discovery_patterns('aem')'        assert 'aem' in aem_patterns'        assert len(aem_patterns['aem']) > 0