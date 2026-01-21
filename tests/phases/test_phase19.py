from pathlib import Path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
import time


def test_phase19() -> None:
    print("--- Phase 19 Verification: Synthetic Data & Signal Bus ---")
    workspace_root = Path(__file__).resolve().parents[2]
    fleet = FleetManager(str(workspace_root))

    # 1. Test Signal Bus
    print("\n[1/2] Testing Signal Bus (Inter-Agent Telepathy)...")
    results = []

    def mock_subscriber(topic, data):
        results.append(data)
        print(f"Subscriber received on {topic}: {data}")

    fleet.signal_bus.subscribe("test_topic", mock_subscriber)
    fleet.signal_bus.publish("test_topic", {"action": "sync", "data": "Hello Swarm"})

    time.sleep(0.5)  # Give it a moment to process
    if results:
        print("✅ Signal Bus confirmed.")
    else:
        print("❌ Signal Bus failed.")

    # 2. Test Synthetic Data Agent
    print("\n[2/2] Testing Synthetic Data Forge...")

    topic = "Python Refactoring"

    # generate_training_data(self, topic: str, count: int = 5)
    training_data = fleet.synthetic_data.generate_training_data(topic, count=3)

    # The agent saves to logs/synthetic_data by default
    expected_path = (
        Path("data/logs/synthetic_data")
        / f"synthetic_{topic.replace(' ', '_').lower()}.jsonl"
    )

    if expected_path.exists():
        print(f"✅ Synthetic data generated at {expected_path}")

        # Cleanup
        # expected_path.unlink()
    else:
        print(f"❌ Synthetic data generation failed. Expected {expected_path}")


if __name__ == "__main__":
    test_phase19()
