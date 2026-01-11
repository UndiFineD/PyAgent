"""
Agents specializing in swarm coordination and fleet-wide management.
"""

from .OrchestratorAgent import OrchestratorAgent

# Backward compatibility (Agent was renamed to OrchestratorAgent)
Agent = OrchestratorAgent
