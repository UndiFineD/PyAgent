
"""
Test script for verifying Copilot backend integration.
"""

import sys
from pathlib import Path

# Robustly find the repository root
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.name != 'src' and project_root.parent != project_root:
    project_root = project_root.parent
if project_root.name == 'src':
    project_root = project_root.parent

# Ensure the project root is in PYTHONPATH
sys.path.insert(0, str(project_root))

from src.infrastructure.compute.backend.llm_backends.copilot_cli_backend import CopilotCliBackend  # pylint: disable=wrong-import-position

def test_copilot():
    """
    Test the Copilot CLI backend integration.
    """
    backend = CopilotCliBackend(None, None) # Mock session/manager
    # Mock _is_working to return True as we don't have a connectivity manager
    # pylint: disable=protected-access
    backend._is_working = lambda x: True
    backend._record = lambda *args, **kwargs: None
    backend._update_status = lambda *args, **kwargs: None

    print("Testing Copilot CLI integration...")
    response = backend.chat("What is 2+2?", timeout_s=10)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_copilot()
