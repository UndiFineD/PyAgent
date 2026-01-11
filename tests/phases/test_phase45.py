import unittest
import os
import shutil
import json
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase45(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath("c:/DEV/PyAgent")
        self.fleet = FleetManager(self.workspace)
        os.makedirs(os.path.join(self.workspace, "data/memory/agent_store/memory_shards"), exist_ok=True)

    def test_graph_relational(self):
        print("\nTesting Graph Relational Agent...")
        self.fleet.graph_relational.add_entity("ByzantineJudge", "SpecializedAgent", {"logic": "AI-Voting"})
        self.fleet.graph_relational.add_entity("FleetManager", "Coordinator")
        res = self.fleet.graph_relational.add_relation("FleetManager", "manages", "ByzantineJudge")
        print(f"Result: {res}")
        self.assertIn("established", res)
        
        rels = self.fleet.graph_relational.query_relationships("FleetManager")
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["target"], "ByzantineJudge")

    def test_memorag_sharding(self):
        print("\nTesting MemoRAG Sharding...")
        self.fleet.memorag.memorise_to_shard("Refactoring the consensus module", "cons_v2")
        shards = self.fleet.memorag.list_shards()
        self.assertIn("cons_v2", shards)
        
        clues = self.fleet.memorag.recall_clues_from_shard("How was consensus updated?", "cons_v2")
        print(f"Clues: {clues}")
        self.assertTrue(any("cons_v2" in clue for clue in clues))

if __name__ == "__main__":
    unittest.main()
