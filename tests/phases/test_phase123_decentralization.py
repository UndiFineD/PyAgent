#!/usr/bin/env python3

import unittest
import json
import os
import shutil
from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.security.ByzantineConsensusAgent import ByzantineConsensusAgent
from src.logic.agents.system.MessagingAgent import MessagingAgent
from src.logic.agents.cognitive.BayesianReasoningAgent import BayesianReasoningAgent
from src.logic.agents.system.LoggingAgent import LoggingAgent
from src.logic.agents.system.IdentityAgent import IdentityAgent as AgentIdentityAgent
from src.infrastructure.orchestration.RLSelector import RLSelector
from pathlib import Path


class TestPhase123Decentralization(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.test_dir = os.path.join(self.root, "test_phase123_work")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        self.fleet = FleetManager(self.root)
        # Register a few dummy agents for committee selection
        self.fleet.register_agent(
            "Coder",
            ByzantineConsensusAgent,
            f"{self.root}/src/agents/ByzantineConsensusAgent.py",
        )
        self.fleet.register_agent(
            "SpecialistA",
            ByzantineConsensusAgent,
            f"{self.root}/src/agents/ByzantineConsensusAgent.py",
        )
        self.fleet.register_agent(
            "SpecialistB",
            ByzantineConsensusAgent,
            f"{self.root}/src/agents/ByzantineConsensusAgent.py",
        )

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_dynamic_committee_formation(self) -> None:
        # Test that FleetManager can form a committee if none provided
        task = "Fix a bug in the quantum logic"
        available = ["Coder", "SpecialistA", "SpecialistB", "Research"]
        judge = ByzantineConsensusAgent(
            f"{self.root}/src/agents/ByzantineConsensusAgent.py"
        )
        committee = judge.select_committee(task, available)

        self.assertTrue(len(committee) > 0)
        self.assertTrue(all(a in available for a in committee))

    def test_messaging_polling_structure(self) -> None:
        # Test that MessagingAgent has poll_for_replies
        import asyncio

        msg_agent = MessagingAgent(f"{self.root}/src/agents/MessagingAgent.py")
        replies = asyncio.run(msg_agent.poll_for_replies("slack"))
        self.assertIsInstance(replies, list)

    def test_bayesian_belief_update(self) -> None:
        # Test that BayesianReasoningAgent updates beliefs correctly
        bayesian = BayesianReasoningAgent(
            f"{self.root}/src/agents/BayesianReasoningAgent.py"
        )
        # Scenario: 50% chance of server up. Evidence: Ping successful (Likelihood 0.9)
        res = bayesian.update_belief("server_up", "ping_success", 0.9)
        self.assertGreater(res["posterior"], 0.5)
        # 2nd Ping:
        res2 = bayesian.update_belief("server_up", "ping_success_2", 0.9)
        self.assertGreater(res2["posterior"], res["posterior"])

    def test_bayesian_rl_selector(self) -> None:
        # Test RLSelector Bayesian logic
        selector = RLSelector()
        selector.update_stats("tool_x", True)
        summary = selector.get_policy_summary()
        self.assertIn("Bayesian Thompson Sampling", summary)
        self.assertIn("tool_x", summary)

    def test_distributed_logging(self) -> None:
        log_file = os.path.join(self.test_dir, "logging_agent.py")
        with open(log_file, "w") as f:
            f.write("#")
        agent = LoggingAgent(log_file)
        # Test configuration
        import asyncio

        res = asyncio.run(
            agent.configure_aggregator(url="http://mock-aggregator:8080/log")
        )
        self.assertIn("Configured", res)

        # Test broadcast
        res = asyncio.run(
            agent.broadcast_log(
                level="INFO",
                source="TestAgent",
                message="Hello World",
                metadata={"phase": 123},
            )
        )
        self.assertIn("Log broadcasted", res)

        # Test integration via BaseAgent
        self.fleet.register_agent("Logging", LoggingAgent, log_file)
        # Registry will create a new instance, ensure it's configured
        logging_agent = self.fleet.agents["Logging"]
        import asyncio

        asyncio.run(
            logging_agent.configure_aggregator(url="http://mock-aggregator:8080/log")
        )

        test_agent = ByzantineConsensusAgent(
            os.path.join(self.test_dir, "test_agent.py")
        )
        test_agent.fleet = self.fleet  # Manual inject for test
        test_agent.log_distributed("WARNING", "Alert message")

        logs = logging_agent.get_aggregated_logs()
        self.assertTrue(any(l["message"] == "Alert message" for l in logs))

    def test_did_sovereign_identity(self) -> None:
        id_file = os.path.join(self.test_dir, "identity_agent.py")
        with open(id_file, "w") as f:
            f.write("#")
        agent = AgentIdentityAgent(id_file)

        # 1. Create DID for Alice
        alice_did = agent.create_agent_did("Alice")
        self.assertTrue(alice_did.startswith("did:pyagent:"))

        # 2. Issue VC from Alice to Bob
        vc = agent.issue_verifiable_credential(
            issuer_name="Alice",
            subject_did="did:pyagent:fleet-01:bob-hash",
            claim_type="AccessBadge",
            claim_value="Level-5",
        )

        self.assertIn("proof", vc)
        self.assertEqual(vc["proof"]["type"], "Ed25519Signature2020")

        # 3. Verify VC
        verification = agent.verify_credential(vc)

        self.assertEqual(verification["status"], "verified")
        self.assertEqual(verification["issuer"], alice_did)

        # 4. Tamper and Verify
        vc_copy = json.loads(json.dumps(vc))

        vc_copy["credentialSubject"]["AccessBadge"] = "Level-99"  # Tamper
        tampered_verification = agent.verify_credential(vc_copy)
        # Signature should fail
        self.assertEqual(tampered_verification["status"], "error")


if __name__ == "__main__":
    unittest.main()
