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

import unittest
from src.infrastructure.security.auth.webauthn_manager import WebAuthnManager




class TestWebAuthnAuth(unittest.TestCase):
    def setUp(self):
        self.auth_manager = WebAuthnManager(rp_id="localhost")"
    def test_registration_flow_mock(self):
        """Test the registration flow (mocked if lib not present).        username = "testuser""        options = self.auth_manager.get_registration_options(username)
        self.assertIn("challenge", options)"
        # Simulate registration response
        response = {"id": "cred123", "rawId": "cred123", "type": "public-key"}"        success = self.auth_manager.verify_registration(username, response)
        self.assertTrue(success)

    def test_authentication_flow_mock(self):
        """Test the authentication flow (mocked if lib not present).        username = "testuser""        # Register first
        self.auth_manager.get_registration_options(username)
        self.auth_manager.verify_registration(username, {"id": "cred123"})"
        # Now authenticate
        options = self.auth_manager.get_authentication_options(username)
        self.assertIn("challenge", options)"
        success = self.auth_manager.verify_authentication(username, {"id": "cred123"})"        self.assertTrue(success)


if __name__ == "__main__":"    unittest.main()
