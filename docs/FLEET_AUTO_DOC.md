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


## 2026-01-16 - Maintenance Cycle Summary (v3.6.0)
The fleet's SelfImprovementOrchestrator completed a Synaptic Acceleration cycle (Phase 317).
- **Complexity Guard**: Scanned 380+ files; identified and refactored high-complexity hotspots.
- **Rust Integration**: 100% of core complexity metrics are now calculated via `rust_core.pyd`.
- **System Stability**: Stability Gate 1.0 achieved after backend hardening.
