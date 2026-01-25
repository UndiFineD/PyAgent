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
Test Phase93 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.ComplianceAuditAgent import ComplianceAuditAgent

class TestComplianceAudit(unittest.TestCase):
    def setUp(self):
        self.agent = ComplianceAuditAgent(os.getcwd())

    def test_compliance_check(self) -> None:
        result = self.agent.run_compliance_check("GDPR")
        self.assertEqual(result['standard'], "GDPR")
        self.assertTrue(result['score'] < 100) # Since we simulate a fail
        self.assertTrue(len(result['failed_checks']) > 0)

    def test_audit_report(self) -> None:
        report = self.agent.generate_audit_report()
        self.assertIn("Compliance Audit Report", report)
        self.assertIn("SOC2", report)
        self.assertIn("GDPR", report)

    def test_invalid_standard(self) -> None:
        result = self.agent.run_compliance_check("NON_EXISTENT")
        self.assertEqual(result['status'], "Error")

if __name__ == "__main__":
    unittest.main()