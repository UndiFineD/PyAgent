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

import shutil
from pathlib import Path
from src.infrastructure.swarm.resilience.distributed_backup import DistributedBackup

def test_raid10_sharding_and_reconstruction():
    backup = DistributedBackup(node_id="test_node_1")

    original_state = {
        "memory": "The secret password is 'voyager'",
        "status": "active",
        "counter": 42,
        "history": ["init", "start", "connect"]
    }

    # Create Shards (Mirror Striping)
    shards = backup.create_shards(original_state)

    # Should have 4 shards (2 parts * 2 mirrors)
    assert len(shards) == 4

    # Simulate losing 50% of shards (specifically the mirrors)
    # Part 0 has mirror 0 and 1. Part 1 has mirror 0 and 1.
    # Keep part 0 mirror 0 and part 1 mirror 1.
    surviving_shards = [shards[0], shards[3]]

    # Reconstruct
    reconstructed = backup.reconstruct_state(surviving_shards)

    assert reconstructed == original_state

    # Clean up
    if Path("data/shards").exists():
        shutil.rmtree("data/shards")

if __name__ == "__main__":
    test_raid10_sharding_and_reconstruction()
    print("RAID-10 Test Passed!")
