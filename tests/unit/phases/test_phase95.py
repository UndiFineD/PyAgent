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
Test Phase95 module.
"""

import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.security.privacy_guard_agent import PrivacyGuardAgent


class TestDataPrivacyGuard(unittest.TestCase):
    def setUp(self):
        self.agent = PrivacyGuardAgent(os.getcwd())

    def test_redaction(self) -> None:
        text = "Hello, my email is john@example.com and phone is 555-0199."
        result = self.agent.scan_and_redact(text)

        self.assertTrue(result["pii_detected"])
        self.assertIn("[REDACTED_EMAIL]", result["redacted"])
        self.assertIn("[REDACTED_PHONE]", result["redacted"])

        self.assertNotIn("john@example.com", result["redacted"])

    def test_safety_check(self) -> None:
        safe_msg = "The weather is lovely today."
        unsafe_msg = "My SSN is 123-456-7890."

        self.assertTrue(self.agent.verify_message_safety(safe_msg)["safe"])
        self.assertFalse(self.agent.verify_message_safety(unsafe_msg)["safe"])

    def test_metrics(self) -> None:
        self.agent.scan_and_redact("contact me at boss@company.org")
        metrics = self.agent.get_privacy_metrics()
        self.assertEqual(metrics["total_redactions"], 1)
        self.assertIn("Email", metrics["pii_types_captured"])


if __name__ == "__main__":
    unittest.main()
