import logging
import sys
from pathlib import Path
from src.classes.fleet.FleetManager import FleetManager

logging.basicConfig(level=logging.INFO)
root = Path("c:/DEV/PyAgent")

try:
    print("Initializing FleetManager...")
    fleet = FleetManager(str(root))
    print("FleetManager initialized successfully.")
    
    # Try accessing a lazy-loaded orchestrator
    print("Accessing scaling (lazy)...")
    scaling = fleet.scaling
    print(f"Scaling manager: {scaling}")
    
    # Try accessing a lazy-loaded agent
    print("Accessing Sandbox agent (lazy)...")
    sandbox = fleet.agents.get("Sandbox")
    print(f"Sandbox agent: {sandbox}")
    
    print("All tests passed!")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
