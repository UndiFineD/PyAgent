<<<<<<< HEAD:test_phase24.py
import sys
=======
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
Test Phase24 module.
"""

>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase24.py
from pathlib import Path
<<<<<<< HEAD:test_phase24.py
<<<<<<< HEAD:test_phase24.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase24.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase24.py

from classes.fleet.FleetManager import FleetManager

def test_phase24() -> None:
    print("--- Phase 24 Verification: Swarm Immortality & Temporal Sharding ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Heartbeat
    print("\n[1/2] Testing Heartbeat Verification...")
    fleet.heartbeat.record_heartbeat("Reasoner")
    if "Reasoner" in fleet.heartbeat.last_seen:
        print("✅ Heartbeat recorded successfully.")
    else:
        print("❌ Heartbeat failed to record.")

    # 2. Test Temporal Sharding
    print("\n[2/2] Testing Temporal Sharding (Flashback)...")
    context = fleet.temporal_shard.retrieve_temporal_context("Verify agent logic")
    if "FLASHBACK" in context:
        print(f"✅ Temporal context retrieved: {context}")
    else:
        print("❌ Temporal sharding failed.")

if __name__ == "__main__":
    test_phase24()