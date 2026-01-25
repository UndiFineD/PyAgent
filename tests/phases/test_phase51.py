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
Test Phase51 module.
"""

import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase51(IsolatedAsyncioTestCase):
    def setUp(self):
        self.fleet = FleetManager(str(Path(__file__).resolve().parents[2]))

    async def test_tenant_isolation(self) -> None:
        print("\nTesting Phase 51: Multi-Tenant Fleet Isolation & Privacy...")
        tenant_a = "Client_A"
        tenant_b = "Client_B"

        # Resource limits
        res = self.fleet.tenant_isolation.set_resource_limits(tenant_a, 10000, 5)
        if asyncio.iscoroutine(res):
            await res
        self.assertIn(tenant_a, self.fleet.tenant_isolation.resource_limits)

        # ZK-Knowledge Sharding
        res = self.fleet.tenant_isolation.encrypt_knowledge_shard(
            tenant_a, "Top secret project alpha"
        )
        if asyncio.iscoroutine(res):
            shard_id = await res
        else:
            shard_id = res
        print(f"Encrypted Shard ID: {shard_id}")
        self.assertIsNotNone(shard_id)

        # Access validation
        res = self.fleet.tenant_isolation.validate_access(
            tenant_a, "Client_A_Resource_01"
        )
        if asyncio.iscoroutine(res):
            is_valid = await res
        else:
            is_valid = res
        self.assertTrue(is_valid)

        res = self.fleet.tenant_isolation.validate_access(
            tenant_a, "Client_B_Resource_01"
        )
        if asyncio.iscoroutine(res):
            is_valid = await res

        else:
            is_valid = res
        self.assertFalse(is_valid)

        # ZK-Fusion
        res = self.fleet.tenant_isolation.encrypt_knowledge_shard(
            tenant_b, "Project beta highlights"
        )
        if asyncio.iscoroutine(res):
            shard_id_2 = await res
        else:
            shard_id_2 = res

        res = self.fleet.tenant_isolation.fuse_knowledge_zk([shard_id, shard_id_2])
        if asyncio.iscoroutine(res):
            fusion_res = await res

        else:
            fusion_res = res
        print(f"Fused Insights: {fusion_res}")
        self.assertIn("Insight from", fusion_res)


if __name__ == "__main__":
    unittest.main()