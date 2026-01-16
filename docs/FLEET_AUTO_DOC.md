# Swarm Auto-Generated Documentation

# Documentation for FleetManager.py

**Module Overview:**
Coordinator for deploying and aggregating results from multiple agents.

## Class: `FleetManager`
The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
agents to complete complex workflows, manages resource scaling, and ensures
system-wide stability through various orchestrators.

### Method: `__getattr__`
Delegate to orchestrators and agents for lazy loading support.

### Method: `__init__`
### Method: `telemetry`
### Method: `registry`
### Method: `signals`
### Method: `recorder`
### Method: `sql_metadata`
### Method: `self_healing`
### Method: `self_improvement`
### Method: `global_context`
### Method: `fallback`
### Method: `core`
### Method: `rl_selector`
### Method: `preempt_lower_priority_tasks`
Suspends all tasks with lower priority than the new high-priority task.

### Method: `resume_tasks`
Resumes all suspended tasks if no critical tasks are running.

### Method: `register_remote_node`
Registers a remote node and its available agents.
Uses VersionGate to ensure compatibility (Phase 104).

### Method: `register_agent`
Adds an agent to the fleet.

### Method: `cell_divide`
Simulates biological mitosis.

### Method: `cell_differentiate`
Changes an agent's characteristics.

### Method: `cell_apoptosis`
Cleanly shuts down and removes an agent.

### Method: `execute_with_consensus`
Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.

### Method: `route_task`
Routes tasks based on system load and hardware availability (Phase 126).


## 2026-01-16 - Maintenance Cycle Summary
The fleet's SelfImprovementOrchestrator completed a cycle over 1046 files. 

### Key Achievements:
- **BaseAgent Modularization**: Successfully refactored `BaseAgent.py` (Complexity: 135) into 5 domain-specific Mixins.
- **Git Synchronization**: Resolved a critical merge conflict in `requirements.txt` and merged 8 legacy restoration branches into `main`.
- **Tool Restoration**: Fixed circular imports in `src/observability/stats` and patched the `SelfImprovementOrchestrator` to handle project-root imports correctly.
- **Debt Reduction**: Verified that 24 identified debt clusters are now queued for autonomous refactoring.

Re-stabilization phase engaged.
