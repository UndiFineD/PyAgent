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


"""
"""
Test module for credential_extraction_agent
"""
try:

"""
import platform
except ImportError:
    import platform

try:
    import pytest
except ImportError:
    import pytest


try:
    from .core.agents.credential_extraction_agent import CredentialExtractionAgent
except ImportError:
    from src.core.agents.credential_extraction_agent import CredentialExtractionAgent



@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
class TestCredentialExtractionAgent:
"""
Test cases for CredentialExtractionAgent.""
def test_init(self):
"""
Test agent initialization.""
agent = CredentialExtractionAgent()
        assert agent is not None

    def test_extract_adsync_credentials_no_adsync(self):
        ""
Test credential extraction when ADSync is not installed.""
agent = CredentialExtractionAgent()
        result = agent.extract_adsync_credentials()

        # Should fail gracefully if ADSync not present
        assert isinstance(result, dict)
        assert "success" in result
        assert "error" in result
