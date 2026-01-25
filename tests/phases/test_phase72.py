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
Test Phase72 module.
"""

import unittest
import os
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase72(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_core_evolution_guard(self) -> None:
        print("\nTesting Phase 72: Agentic Self-Evolution & Core Hardening...")

        # Test file
        test_file = os.path.join("src", "logic", "agents", "system", "core_evolution_guard.py")

        # Take snapshot

        res = self.fleet.evolution_guard.snapshot_core_logic([test_file])
        print(f"Snapshot Result: {res}")
        self.assertEqual(res["monitored_files"], 1)

        # Validate (no change)
        val_res = self.fleet.evolution_guard.validate_code_integrity(test_file)
        print(f"Validation Result (No Change): {val_res}")
        self.assertEqual(val_res["status"], "unchanged")

        # Validate (untracked)
        untracked_res = self.fleet.evolution_guard.validate_code_integrity(
            "nonexistent.py"
        )
        print(f"Validation Result (Untracked): {untracked_res}")
        self.assertEqual(untracked_res["status"], "untracked")

        # Report
        report = self.fleet.evolution_guard.generate_hardening_report()
        print(f"Hardening Report: {report}")
        self.assertEqual(report["monitored_files_count"], 1)


if __name__ == "__main__":
    unittest.main()