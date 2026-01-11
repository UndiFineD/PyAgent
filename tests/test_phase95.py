import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.specialized.DataPrivacyGuardAgent import DataPrivacyGuardAgent

class TestDataPrivacyGuard(unittest.TestCase):
    def setUp(self):
        self.agent = DataPrivacyGuardAgent(os.getcwd())

    def test_redaction(self) -> None:
        text = "Hello, my email is john@example.com and phone is 555-0199."
        result = self.agent.scan_and_redact(text)
        
        self.assertTrue(result['pii_detected'])
        self.assertIn("[REDACTED_EMAIL]", result['redacted'])
        self.assertIn("[REDACTED_PHONE]", result['redacted'])
        self.assertNotIn("john@example.com", result['redacted'])

    def test_safety_check(self) -> None:
        safe_msg = "The weather is lovely today."
        unsafe_msg = "My SSN is 123-456-7890."
        
        self.assertTrue(self.agent.verify_message_safety(safe_msg))
        self.assertFalse(self.agent.verify_message_safety(unsafe_msg))

    def test_metrics(self) -> None:
        self.agent.scan_and_redact("contact me at boss@company.org")
        metrics = self.agent.get_privacy_metrics()
        self.assertEqual(metrics['total_redactions'], 1)
        self.assertIn("Email", metrics['pii_types_captured'])

if __name__ == "__main__":
    unittest.main()
