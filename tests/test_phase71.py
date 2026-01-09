import unittest
import os
import json
from src.classes.fleet.FleetManager import FleetManager

class TestPhases71(unittest.TestCase):
    def setUp(self):
        self.workspace = "c:/DEV/PyAgent"
        self.fleet = FleetManager(self.workspace)

    def test_process_synthesizer(self):
        print("\nTesting Phase 71: Neural Process Orchestration...")
        goal = "Fix authentication bug in dashboard"
        reqs = ["Secure session handling", "JWT validation"]
        
        synth_res = self.fleet.process_synthesizer.synthesize_workflow(goal, reqs)
        print(f"Synthesis Result: {synth_res}")
        self.assertIn("workflow_id", synth_res)
        
        flow_id = synth_res["workflow_id"]
        opt_res = self.fleet.process_synthesizer.optimize_step(flow_id, 0)
        print(f"Optimization Result: {opt_res}")
        self.assertEqual(opt_res["status"], "optimized")
        
        telemetry = self.fleet.process_synthesizer.get_workflow_telemetry(flow_id)
        print(f"Workflow Telemetry: {telemetry}")
        self.assertEqual(telemetry["status"], "active")

    def test_cooperative_comm(self):
        print("\nTesting Cooperative Communication Integration...")
        chan_res = self.fleet.cooperative_comm.establish_p2p_channel("Agent1", "Agent2")
        print(f"Channel Result: {chan_res}")
        self.assertIn("channel_id", chan_res)
        
        broadcast = self.fleet.cooperative_comm.broadcast_thought_packet("Agent1", {"signal": "start_refactor"})
        print(f"Broadcast Result: {broadcast}")
        self.assertEqual(broadcast["status"], "broadcast_complete")

if __name__ == "__main__":
    unittest.main()
