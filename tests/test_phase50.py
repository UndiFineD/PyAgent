import unittest
from fastapi.testclient import TestClient
from src.classes.api.AgentAPIServer import app

class TestPhase50(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_api_endpoints(self) -> None:
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
            "context": {}
        }
        res = self.client.post("/task", json=task_data)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        print(f"Task result: {data}")
        self.assertEqual(data["status"], "success")

if __name__ == "__main__":
    unittest.main()
