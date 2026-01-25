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

#!/usr/bin/env python3
"""Integration tests for the agent interaction pipeline."""

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


def test_pipeline() -> None:
    print("=== Testing Interaction Harvesting Pipeline ===")
    fleet = FleetManager(".")

    # 1. Record some fake interactions
    print("Step 1: Recording interactions...")
    for i in range(10):
        # Using the actual method name and params from LocalContextRecorder
        fleet.recorder.record_interaction(
            provider="TestProvider",
            model="test-model",
            prompt=f"Test prompt {i}",
            result="Success output" if i % 2 == 0 else "Error: failed",
            meta={
                "id": f"test_id_{i}",
                "agent": "TestAgent",
                "type": "unit_test",
                "status": "success" if i % 2 == 0 else "failed",
                "tags": ["test", "demo", f"num_{i}"],
            },
        )

    # 2. Force sharding index update (the recorder does this)
    # 3. Use SqlAgent to index
    print("Step 2: Indexing metadata into SQL...")

    indexed = fleet.sql_metadata.index_shards()
    print(f"Indexed {indexed} items.")

    # 4. Query back
    print("Step 3: Querying SQL...")

    results = fleet.sql_metadata.query_interactions(
        "success = 1 AND task_type = 'unit_test'"
    )
    print(f"Found {len(results)} successful unit tests.")
    for res in results:
        print(f" - ID: {res['id']}, Status: {res['success']}")

    if len(results) >= 5:
        print("PIPELINE TEST PASSED!")
    else:
        print("PIPELINE TEST FAILED - Results incomplete.")


if __name__ == "__main__":
    test_pipeline()
