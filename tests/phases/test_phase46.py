import unittest
import os
import json
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase46(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Setup shared state file location
        self.state_file = os.path.join(self.workspace, "data/memory/agent_store/quantum_state.json")
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    def test_quantum_entanglement(self) -> None:
        print("\nTesting Quantum Shard Entanglement...")
        # Shard A updates state
        resA = self.fleet.quantum_shard.update_entangled_state("consensus_protocol", "BFT-2.1")
        print(f"Shard A update: {resA}")
        
        # Shard B measures state (instantly synchronized via the 'field')
        valB = self.fleet.quantum_shard.measure_state("consensus_protocol")
        print(f"Shard B measurement: {valB}")
        self.assertEqual(valB, "BFT-2.1")

    def test_binary_bridge_transmission(self) -> None:
        print("\nTesting High-Throughput Bridge...")
        dummy_packet = b"\x00\xFF\xAA\x55" * 1024 # 4KB bin packet
        success = self.fleet.inter_fleet_bridge.transmit_binary_packet(dummy_packet)
        self.assertTrue(success)
        
        self.fleet.inter_fleet_bridge.toggle_quantum_sync(True)

if __name__ == "__main__":
    unittest.main()
