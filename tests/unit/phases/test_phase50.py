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
Test Phase50 module.
"""

import unittest
from fastapi.testclient import TestClient
from src.infrastructure.services.api.agent_api_server import app


class TestPhase50(unittest.TestCase):
    """Test cases for Phase 50: API Endpoints (TestClient)."""
    def setUp(self):
        self.client = TestClient(app)

    def test_api_endpoints(self) -> None:
        """Test API endpoints using TestClient."""
        print("\nTesting Phase 50: API Endpoints (TestClient)...")
        # Test Root
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        print(f"Root: {data}")
        self.assertIn("online", data["status"])

        # Test Agents
        res = self.client.get("/agents")

        self.assertEqual(res.status_code, 200)
        data = res.json()
        print(f"Agents: {len(data['agents'])} found")
        agent_ids = [a["id"] for a in data["agents"]]

        self.assertIn("Telemetry", agent_ids)
        self.assertIn("FleetDeployer", agent_ids)

        # Test Task Dispatch
        task_data = {
            "agent_id": "LinguisticAgent",
            "task": "Translate 'Hello' to French",
            "context": {},
        }
        res = self.client.post("/task", json=task_data)

        self.assertEqual(res.status_code, 200)
        data = res.json()
        print(f"Task result: {data}")
        self.assertEqual(data["status"], "success")


if __name__ == "__main__":
    unittest.main()
