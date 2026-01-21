import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.security.security_audit_agent import SecurityAuditAgent


class TestSecurityAudit(unittest.TestCase):
    def setUp(self):
        self.agent = SecurityAuditAgent(os.getcwd())
        self.test_file = "test_security_audit.py"

        with open(self.test_file, "w") as f:
            f.write("api_key = 'sk-12345'\n")
            f.write("eval('print(1)')\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_scan_file(self) -> None:
        findings = self.agent.scan_file(self.test_file)
        self.assertTrue(any(f["type"] == "Hardcoded Secret" for f in findings))
        self.assertTrue(
            any(
                f["type"] == "Insecure Pattern" and "eval" in f["detail"]
                for f in findings
            )
        )

    def test_audit_workspace(self) -> None:
        # Full scan might take time but should return findings due to our test file
        result = self.agent.audit_workspace()
        self.assertEqual(result["status"], "Complete")
        self.assertTrue(result["findings_count"] > 0)


if __name__ == "__main__":
    unittest.main()
