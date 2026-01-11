import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.fleet.FleetManager import FleetManager

class TestExplainability(unittest.TestCase):
    def setUp(self):
        self.fleet = FleetManager(os.getcwd())

    def test_explainability_trace(self) -> None:
        workflow = [
            {"agent": "PrivacyGuard", "action": "scan_and_redact", "args": ["My email is test@example.com"]}
        ]
        
        # Run workflow
        report = self.fleet.execute_workflow("Explainability Test", workflow)
        
        # Get workflow ID from the report or internal state
        workflow_id = self.fleet.state.task_id
        
        # Get explanation
        explanation = self.fleet.explainability.get_explanation(workflow_id)
        
        self.assertIn("Explainability Report", explanation)
        self.assertIn("PrivacyGuard.scan_and_redact", explanation)
        self.assertIn("GDPR compliance", explanation) # From our mock justification

    def test_justification_logic(self) -> None:
        agent_name = "SecurityAudit"
        action = "scan_file"
        justification = self.fleet.explainability.justify_action(agent_name, action, {})
        self.assertIn("catastrophic leaks", justification)

if __name__ == "__main__":
    unittest.main()
