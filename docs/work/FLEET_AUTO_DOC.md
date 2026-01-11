# Swarm Auto-Generated Documentation

## 🏗️ Specialized Agent Registry (Phase 121/122 Updates)

This registry provides an overview of the "Realized" specialized agents that have graduated from mocks to functional, AI-driven components.

### 1. `SpecToolAgent`
- **Purpose**: Generates dynamic HTTP/REST client tools from OpenAPI/Swagger specifications.
- **Key Tools**:
  - `generate_tool_from_spec(spec_json)`: Produces a fully functional Python class with `requests` logic for interacting with a specific API.

### 2. `MessagingAgent`
- **Purpose**: Real-time communication hub for webhooks, Slack, and Discord.
- **Key Tools**:
  - `send_notification(platform, recipient, message)`: Sends messages via webhooks.
  - `poll_for_replies(platform)`: Polls Slack/Discord APIs for inbound replies (Phase 123).

### 3. `ByzantineConsensusAgent`
- **Purpose**: Fault-tolerant decision making using weighted reputation scoring.
- **Key Tools**:
  - `select_committee(task, available_agents)`: Dynamically selects committee members based on task requirements (Phase 123).
  - `run_committee_vote(task, proposals)`: Aggregates multiple agent outputs and selects the optimal one based on verified reputation.

### 4. `MultiModalContextAgent`
- **Purpose**: Hybrid computer vision and environment analysis.
- **Key Tools**:
  - `process_visual_input(image_path)`: Uses cloud LLM Vision or local Tesseract OCR to extract context from images.
  - `analyze_workspace_complexity()`: Combines visual file structure maps with metric analysis.

### 5. `TemporalPredictorAgent`
- **Purpose**: AI-driven predictive maintenance and anomaly detection.
- **Key Tools**:
  - `predict_next_failure(logs)`: Analyzes sequence patterns to anticipate system bottlenecks or security breaches.

### 6. `ImmuneSystemAgent`
- **Purpose**: Autonomous health monitoring and vulnerability patching.
- **Key Tools**:
  - `scan_for_vulnerabilities(file_content)`: Identifies injections, path traversal, and misconfigurations.
  - `propose_autonomous_patch(report, code)`: Generates AI-verified fixes for security issues.

### 7. `VisualizerAgent`
- **Purpose**: Real-time fleet health and topology streaming.
- **Key Tools**:
  - `generate_3d_swarm_data()`: Produces JSON streams for 3D force-directed graph frontends.

### 8. `AgentIdentityAgent`
- **Purpose**: Decentralized Identity (DID) and Verifiable Credential (VC) management.
- **Key Tools**:
  - `create_agent_did(name)`: Issues global DIDs for agents.
  - `verify_credential(vc)`: Cryptographically ensures the origin and integrity of instructions via `SecretManager`.

### 9. `ProactiveAgent`
- **Purpose**: Anticipatory task execution and user habit recognition.
- **Key Tools**:
  - `get_habit_recommendation(user_history)`: Analyzes log patterns to suggest automated optimizations (Phase 123).
  - `schedule_task(...)`: Managed future execution of recurring workflows.

### 10. `BayesianReasoningAgent`
- **Purpose**: Decision-making under uncertainty using probabilistic inference.
- **Key Tools**:
  - `update_belief(concept, evidence, likelihood)`: Updates posterior probabilities using Bayes' Theorem.
  - `calculate_expected_utility(actions)`: Multi-objective optimization for fleet actions.

---

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
Records the unique context, prompt and result for future reference.

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
Simulates biological mitosis by creating a clone of an existing agent.

### Method: `cell_differentiate`
Changes an agent's characteristics or 'role' based on environmental signals.

### Method: `cell_apoptosis`
Cleanly shuts down and removes an agent from the fleet (programmed cell death).

### Method: `execute_workflow`
Runs a sequence of agent actions with shared state and signals.

### Method: `execute_with_consensus`
Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
Useful for high-integrity changes. (Phase 41)


## 2026-01-10 - Maintenance Cycle Summary
The fleet's SelfImprovementOrchestrator completed a cycle over 859 files. Re-stabilization phase engaged.
