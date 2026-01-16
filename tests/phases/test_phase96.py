import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase

# Ensure the project root is in PYTHONPATH

from src.infrastructure.fleet.FleetManager import FleetManager


class TestExplainability(IsolatedAsyncioTestCase):
    def setUp(self):
        self.fleet = FleetManager(os.getcwd())

    async def test_explainability_trace(self) -> None:
        workflow = [
            {
                "agent": "PrivacyGuard",
                "action": "scan_and_redact",
                "args": ["My email is test@example.com"],
            }
        ]

        # Run workflow
        res = self.fleet.execute_workflow("Explainability Test", workflow)
        if asyncio.iscoroutine(res):
            report = await res
        else:
            report = res

        # Get workflow ID from the report or internal state
        workflow_id = self.fleet.state.task_id

        # Get explanation
        # explanation might be async too
        res = self.fleet.explainability.get_explanation(workflow_id)

        if asyncio.iscoroutine(res):
            explanation = await res
        else:
            explanation = res

        self.assertIn("Explainability Report", explanation)
        self.assertIn("PrivacyGuard.scan_and_redact", explanation)
        self.assertIn("GDPR compliance", explanation)  # From our mock justification

    async def test_justification_logic(self) -> None:
        agent_name = "SecurityAudit"
        action = "scan_file"
        res = self.fleet.explainability.justify_action(agent_name, action, {})
        if asyncio.iscoroutine(res):
            justification = await res
        else:
            justification = res
        self.assertIn("catastrophic leaks", justification)


if __name__ == "__main__":
    unittest.main()
