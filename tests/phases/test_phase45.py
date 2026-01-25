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
Test Phase45 module.
"""

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