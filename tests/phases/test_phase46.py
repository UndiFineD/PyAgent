import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.fleet.fleet_manager import FleetManager


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
