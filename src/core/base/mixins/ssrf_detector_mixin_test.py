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


from src.core.base.mixins.ssrf_detector_mixin import SSRFDetectorMixin


class TestSSRFDetectorMixin:
    """Test cases for SSRFDetectorMixin."""
    def setup_method(self):
        self.mixin = SSRFDetectorMixin()

    def test_token_generation(self):
        """Test token generation."""token1 = self.mixin.get_ssrf_token()
        token2 = self.mixin.reset_ssrf_token()
        assert len(token1) == 16
        assert len(token2) == 16
        assert token1 != token2

    def test_detector_lifecycle(self):
        """Test starting and stopping detector."""# Start detector
        success = self.mixin.start_ssrf_detector(port=0)  # Use port 0 for auto-assignment
        assert success
        assert self.mixin.is_detector_running()

        # Stop detector
        self.mixin.stop_ssrf_detector()
        assert not self.mixin.is_detector_running()

    def test_callback_url_generation(self):
        """Test callback URL generation."""url = self.mixin.get_ssrf_callback_url('example.com', 8080)'        assert 'http://example.com:8080/' in url'        assert len(self.mixin.get_ssrf_token()) == 16

    def test_data_collection(self):
        """Test data collection from callbacks."""# Start detector
        self.mixin.start_ssrf_detector(port=0)

        try:
            # Simulate callback
            self.mixin.get_ssrf_token()
            self.mixin._ssrf_data['test'] = ['value1']'
            # Check data
            data = self.mixin.check_ssrf_triggered('test', timeout=0)'            assert 'value1' in data'
            # Clear data
            self.mixin.clear_ssrf_data()
            assert len(self.mixin._ssrf_data) == 0

        finally:
            self.mixin.stop_ssrf_detector()

    def test_async_check(self):
        """Test async SSRF check."""import asyncio

        async def run():
            # Start detector
            self.mixin.start_ssrf_detector(port=0)

            try:
                # Simulate data
                self.mixin._ssrf_data['async_test'] = ['async_value']'
                # Check async
                data = await self.mixin.async_check_ssrf_triggered('async_test', timeout=0)'                assert 'async_value' in data'
            finally:
                self.mixin.stop_ssrf_detector()

        asyncio.run(run())
