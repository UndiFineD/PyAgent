#!/usr/bin/env python3
"""Integration tests for the agent interaction pipeline."""

from src.infrastructure.fleet.FleetManager import FleetManager


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
