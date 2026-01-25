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
Test Phase71 module.
"""
<<<<<<< HEAD:tests/test_phase71.py
=======

import unittest
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase71.py

import unittest
import os
import json
from src.classes.fleet.FleetManager import FleetManager

class TestPhases71(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_process_synthesizer(self) -> None:
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

    def test_cooperative_comm(self) -> None:
        print("\nTesting Cooperative Communication Integration...")
        chan_res = self.fleet.cooperative_comm.establish_p2p_channel("Agent1", "Agent2")
        print(f"Channel Result: {chan_res}")
        self.assertIn("channel_id", chan_res)
        
        broadcast = self.fleet.cooperative_comm.broadcast_thought_packet("Agent1", {"signal": "start_refactor"})
        print(f"Broadcast Result: {broadcast}")
        self.assertEqual(broadcast["status"], "broadcast_complete")

if __name__ == "__main__":
    unittest.main()