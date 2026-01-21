import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase45(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        os.makedirs(
            os.path.join(self.workspace, "data/memory/agent_store/memory_shards"),
            exist_ok=True,
        )

    async def test_graph_relational(self) -> None:
        print("\nTesting Graph Relational Agent...")
        # Add entities (assuming sync or async, handling both)
        res = self.fleet.graph_relational.add_entity(
            "ByzantineJudge", "SpecializedAgent", {"logic": "AI-Voting"}
        )
        if asyncio.iscoroutine(res):
            await res

        res = self.fleet.graph_relational.add_entity("FleetManager", "Coordinator")
        if asyncio.iscoroutine(res):
            await res

        res = self.fleet.graph_relational.add_relation(
            "FleetManager", "manages", "ByzantineJudge"
        )
        if asyncio.iscoroutine(res):
            res = await res
        print(f"Result: {res}")
        self.assertIn("established", res)

        rels = self.fleet.graph_relational.query_relationships("FleetManager")
        if asyncio.iscoroutine(rels):
            rels = await rels

        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["target"], "ByzantineJudge")

    async def test_memorag_sharding(self) -> None:
        print("\nTesting MemoRAG Sharding...")
        res = self.fleet.memorag.memorise_to_shard(
            "Refactoring the consensus module", "cons_v2"
        )
        if asyncio.iscoroutine(res):
            await res

        shards = self.fleet.memorag.list_shards()

        if asyncio.iscoroutine(shards):
            shards = await shards
        self.assertIn("cons_v2", shards)

        clues = self.fleet.memorag.recall_clues_from_shard(
            "How was consensus updated?", "cons_v2"
        )

        if asyncio.iscoroutine(clues):
            clues = await clues
        print(f"Clues: {clues}")
        self.assertTrue(any("cons_v2" in clue for clue in clues))


if __name__ == "__main__":
    unittest.main()
