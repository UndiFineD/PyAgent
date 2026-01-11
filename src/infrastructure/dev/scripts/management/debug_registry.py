"""Debug script for inspecting the agent registry."""

from src.infrastructure.fleet.FleetManager import FleetManager
import os

f = FleetManager(os.getcwd())
print(f"Agents in registry: {len(f.agents.keys())}")
print(f"Sample: {f.agents.keys()[:5]}")
print(f"Has CooperativeCommunication? {'CooperativeCommunication' in f.agents}")
print(f"Has cooperative_communication? {'cooperative_communication' in f.agents}")
