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
Test Phase46 module.
"""

import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase46(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Setup shared state file location
        self.state_file = os.path.join(
            self.workspace, "data/memory/agent_store/quantum_state.json"
        )
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    async def test_quantum_entanglement(self) -> None:
        print("\nTesting Quantum Shard Entanglement...")
        # Shard A updates state
        resA = self.fleet.quantum_shard.update_entangled_state(
            "consensus_protocol", "BFT-2.1"
        )
        if asyncio.iscoroutine(resA):
            resA = await resA
        print(f"Shard A update: {resA}")

        # Shard B measures state (instantly synchronized via the 'field')
        valB = self.fleet.quantum_shard.measure_state("consensus_protocol")
        if asyncio.iscoroutine(valB):
            valB = await valB

        print(f"Shard B measurement: {valB}")
        self.assertEqual(valB, "BFT-2.1")

    async def test_binary_bridge_transmission(self) -> None:
        print("\nTesting High-Throughput Bridge...")

        dummy_packet = b"\x00\xff\xaa\x55" * 1024  # 4KB bin packet
        success = self.fleet.inter_fleet_bridge.transmit_binary_packet(dummy_packet)
        if asyncio.iscoroutine(success):
            success = await success
        self.assertTrue(success)

        res = self.fleet.inter_fleet_bridge.toggle_quantum_sync(True)
        if asyncio.iscoroutine(res):
            await res


if __name__ == "__main__":
    unittest.main()