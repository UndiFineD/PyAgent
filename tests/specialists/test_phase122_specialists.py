import sys
import os
import unittest
import asyncio
from unittest.mock import patch
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.infrastructure.fleet.secret_manager import SecretManager
from src.logic.agents.security.immune_system_agent import ImmuneSystemAgent
from src.logic.agents.cognitive.visualizer_agent import VisualizerAgent
from src.logic.agents.system.identity_agent import IdentityAgent as AgentIdentityAgent


class TestPhase122Specialists(unittest.TestCase):
    def setUp(self):
        self.vault_file = "data/memory/agent_store/test_vault.json"
        if os.path.exists(self.vault_file):
            os.remove(self.vault_file)
        self.sm = SecretManager(provider="file", vault_path=self.vault_file)

    def tearDown(self):
        if os.path.exists(self.vault_file):
            os.remove(self.vault_file)

    def test_secret_manager_persistence(self) -> None:
        """Test that secrets are persisted to the local file vault."""
        self.sm.set_secret("TEST_KEY", "secret_value", persist=True)

        # Create a new manager pointing to the same file
        sm2 = SecretManager(provider="file", vault_path=self.vault_file)
        self.assertEqual(sm2.get_secret("TEST_KEY"), "secret_value")

    def test_visualizer_3d_data(self) -> None:
        """Test that VisualizerAgent generates correct 3D schema."""
        va = VisualizerAgent("dummy.py")
        data = va.generate_3d_swarm_data()
        self.assertEqual(data["format"], "v1-3d-swarm")
        self.assertTrue(len(data["nodes"]) > 0)
        self.assertTrue(len(data["links"]) > 0)

    from unittest.mock import patch, AsyncMock
    import asyncio

    @patch("src.core.base.base_agent.BaseAgent.think", new_callable=AsyncMock)
    def test_immune_system_patching(self, mock_think) -> None:
        """Test that ImmuneSystemAgent can propose a patch via LLM."""
        mock_think.return_value = "FIXED_CODE_HERE"
        isa = ImmuneSystemAgent("dummy.py")

        patch_code = asyncio.run(isa.propose_autonomous_patch(
            "Injection vulnerability", "def insecure(): pass"
        ))
        self.assertIn("FIXED_CODE_HERE", patch_code)
        self.assertIn("### Autonomous Security Patch Proposal", patch_code)
        mock_think.assert_called_once()

    def test_agent_identity_with_secrets(self) -> None:
        """Test that AgentIdentityAgent uses SecretManager for VCs."""
        aia = AgentIdentityAgent("dummy.py")
        # Set a custom secret in the manager AIA uses

        aia.secret_manager.set_secret(
            "AGENT_IDENTITY_SECRET", "test-secret", persist=True
        )

        did = aia.create_agent_did("TestAgent")
        vc = aia.issue_verifiable_credential(did, did, "TestType", "TestValue")

        self.assertIn("proof", vc)
        # Verification should pass
        verification = aia.verify_credential(vc)
        self.assertEqual(verification["status"], "verified")


if __name__ == "__main__":
    unittest.main()
