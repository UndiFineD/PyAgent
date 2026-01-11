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
### Method: `execute_reliable_task`
Executes a task using the 7-phase inner loop and linguistic articulation.

### Method: `_record_success`
Records the success of a workflow step including Explainability and Telemetry.

### Method: `_record_failure`
Records errors, failures, and mistakes for collective intelligence (Phase 108).

### Method: `register_remote_node`
Registers a remote node and its available agents.
Uses VersionGate to ensure compatibility (Phase 104).

### Method: `call_by_capability`
Finds an agent with the required capability and executes it with RL optimization.

### Method: `register_agent`
Adds an agent to the fleet.

### Method: `cell_divide`
Simulates biological mitosis.

### Method: `cell_differentiate`
Changes an agent's characteristics.

### Method: `cell_apoptosis`
Cleanly shuts down and removes an agent.

### Method: `execute_workflow`
Runs a sequence of agent actions with shared state and signals.

### Method: `execute_with_consensus`
Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
If agents are not specified, ByzantineConsensusAgent dynamically selects a committee. (Phase 123)

### Method: `route_task`
Routes tasks based on system load and hardware availability (Phase 126).


## 2026-01-11 - Maintenance Cycle Summary
The fleet's SelfImprovementOrchestrator completed a cycle over 62 files. Re-stabilization phase engaged.
