
import pytest
import asyncio
import logging
from pathlib import Path
from src.infrastructure.swarm.orchestration.swarm.director_agent import DirectorAgent

@pytest.mark.asyncio
async def test_status_update():
    # Setup a mock improvements file
    test_file = Path("docs/prompt/test_improvements.md")
    test_file.write_text("""
### High Priority

1. **Test Improvement Task**
   - Status: PLANNED
   - Goal: Test the automation
""", encoding="utf-8")

    try:
        agent = DirectorAgent(str(test_file))
        print(f"Initial status in file: {test_file.read_text()}")

        # Manually trigger the status update logic
        agent._update_improvement_status("Test Improvement Task", "COMPLETED")

        updated_content = test_file.read_text()
        print(f"Updated status in file: {updated_content}")

        if "Status: COMPLETED" in updated_content:
            print("SUCCESS: Status updated correctly.")
        else:
            print("FAILURE: Status not updated.")

    finally:
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_status_update())
