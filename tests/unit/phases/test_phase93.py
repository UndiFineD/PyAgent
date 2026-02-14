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

# Ensure the project root is in PYTHONPATH

from src.logic.agents.security.compliance_audit_agent import ComplianceAuditAgent


class TestComplianceAudit(unittest.TestCase):
    """Unit tests for the ComplianceAuditAgent."""
    def setUp(self):
        """Set up the ComplianceAuditAgent for testing."""
        self.agent = ComplianceAuditAgent(os.getcwd())

    def test_compliance_check(self) -> None:
        """Test running a compliance check for a specific standard."""
        result = self.agent.run_compliance_check("GDPR")
        self.assertEqual(result["standard"], "GDPR")
        self.assertTrue(result["score"] < 100)  # Since we simulate a fail
        self.assertTrue(len(result["failed_checks"]) > 0)

    def test_audit_report(self) -> None:
        """Test generating a compliance audit report."""
        report = self.agent.generate_audit_report()
        self.assertIn("Compliance Audit Report", report)
        self.assertIn("SOC2", report)
        self.assertIn("GDPR", report)

    def test_invalid_standard(self) -> None:
        """Test running a compliance check with an invalid standard."""
        result = self.agent.run_compliance_check("NON_EXISTENT")
        self.assertEqual(result["status"], "Error")


if __name__ == "__main__":
    unittest.main()
