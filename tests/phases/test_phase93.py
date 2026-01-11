import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.logic.agents.security.ComplianceAuditAgent import ComplianceAuditAgent

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
