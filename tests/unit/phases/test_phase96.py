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
Test Phase96 module.
"""

import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase

# Ensure the project root is in PYTHONPATH

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


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
            await res
        else:
            pass

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
