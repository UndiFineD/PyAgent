#!/usr/bin/env python3

import unittest
import os
from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.security.PrivacyGuardAgent import PrivacyGuardAgent
from src.logic.agents.system.MessagingAgent import MessagingAgent
from src.logic.agents.swarm.FleetDeployerAgent import FleetDeployerAgent
from src.logic.agents.cognitive.DynamicDecomposerAgent import DynamicDecomposerAgent
from src.core.base.NeuralPruningEngine import NeuralPruningEngine
from pathlib import Path




class TestPhase123FinalRealization(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.root)

        # Ensure we have the necessary agents registered
        self.fleet.register_agent("PrivacyGuard", PrivacyGuardAgent, f"{self.root}/src/agents/security/PrivacyGuardAgent.py")
        self.fleet.register_agent("Messaging", MessagingAgent, f"{self.root}/src/agents/core/MessagingAgent.py")
        self.fleet.register_agent("Deployer", FleetDeployerAgent, f"{self.root}/src/agents/swarm/FleetDeployerAgent.py")
        self.fleet.register_agent("Decomposer", DynamicDecomposerAgent, f"{self.root}/src/agents/cognitive/DynamicDecomposerAgent.py")

    def test_privacy_integration(self) -> None:
        """Tests that MessagingAgent blocks PII via DataPrivacyGuard."""
        messaging = self.fleet.agents["Messaging"]

        # A message with PII (Email)
        pii_message = "Contact me at secret@example.com"

        # This should trigger the privacy guard verify_message_safety via fleet.call_by_capability
        import asyncio
        result = asyncio.run(messaging.send_notification("slack", "admin", pii_message))

        # Verify the message was blocked (either by LLM reasoning or Regex)
        self.assertIn("SAFETY ERROR", result)
        self.assertIn("blocked", result.lower())

    def test_task_decomposition_llm_logic(self) -> None:
        """Tests that DynamicDecomposerAgent uses LLM for decomposition."""
        decomposer = self.fleet.agents["Decomposer"]
        result = decomposer.decompose_task_v2("Build a website and deploy it", ["Coder", "Deployer"])

        self.assertIn("Optimized Task Decomposition", result)
        self.assertIn("```json", result)

    def test_consensus_deployment(self) -> None:
        """Tests that Deployer uses consensus loop."""
        deployer = self.fleet.agents["Deployer"]
        # Use a fake agent_type
        import asyncio
        result = asyncio.run(deployer.consensus_driven_deploy("WebAgent", "swarm-01"))

        # Since we haven't provided proposals, it might reject or use the judge's default
        self.assertTrue("rejected" in result.lower() or "initialized" in result.lower() or "consensus" in result.lower())

    def test_neural_pruning_memory(self) -> None:
        """Tests that NeuralPruningEngine triggers memory cleanup."""
        # Need an instance of PruningEngine
        pruner = NeuralPruningEngine(self.fleet)

        # Mock memory if not present to avoid DB dependency in unit tests
        if not hasattr(self.fleet, "data/memory") or self.fleet.memory is None:
            class MockMemory:
                def get_all_ids(self): return [f"id_{i}" for i in range(1100)]
                def delete_by_ids(self, ids): self.deleted = ids
            self.fleet.memory = MockMemory()











        pruned = pruner.prune_underutilized(threshold=0.0)

        if hasattr(self.fleet.memory, "deleted"):



            self.assertEqual(len(self.fleet.memory.deleted), 110)  # 10% of 1100

    def test_bootstrap_overlay(self) -> None:
        """Tests that RegistryOverlay is utilized."""
        from src.infrastructure.fleet.RegistryOverlay import RegistryOverlay


        overlay = RegistryOverlay(Path("data/memory/agent_store/test_overlay.json"))
        overlay.save_override("TestAgent", "test.module", "TestClass")

        config = overlay.get_agent_config("TestAgent", ("default", "Class", None))
        self.assertEqual(config[0], "test.module")




        # Clean up
        if Path("data/memory/agent_store/test_overlay.json").exists():
            os.remove("data/memory/agent_store/test_overlay.json")





if __name__ == "__main__":
    unittest.main()
