# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# PyAgent Agent Workflow Design

## Overview

This document details the proposed workflow design for agents within the PyAgent system. The workflow defines the end-to-end processing sequence that each agent follows when executing a task.

## Core Workflow Phases

### 1. Task Initialization and Receipt

- **Task Arrival**:
  - Task message is received from the central task queue
  - Message is parsed to extract task metadata, context, and requirements
  - Message is validated against system constraints and availability rules

- **Initial Processing**:
  - Task is validated for correctness and feasibility
  - Contextual information is extracted and parsed
  - Task is categorized by type and complexity level

- **Queue Assignment**:
  - Task is routed to the appropriate agent pool based on task type
  - Task priority is assigned based on urgency and complexity

### 2. Context Analysis and Planning

- **Context Extraction**:
  - Critical information from the task context is identified
  - Constraints, dependencies, and boundary conditions are extracted
  - Historical data and patterns are retrieved for context

- **Problem Understanding**:
  - Task requirements are analyzed to understand the problem space
  - Key objectives, success criteria, and failure conditions are defined
  - Potential challenges and risks are identified

- **Strategy Formulation**:
  - Processing strategy is developed based on task characteristics
  - Step-by-step approach is defined with clear decision points
  - Resource allocation plan is created

### 3. Execution and Processing

- **Step-by-Step Execution**:
  - Processing is carried out in defined steps according to the strategy
  - Each step is monitored for progress and completion
  - Intermediate results are collected and stored

- **Intermediate Checks**:
  - Periodic validation of processing state
  - Progress tracking against defined milestones
  - Error detection and early termination if critical issues detected

- **Resource Management**:
  - Memory and computational resources are allocated dynamically
  - Resource usage is monitored to prevent overconsumption
  - Resource cleanup is performed at task completion

### 4. Result Generation and Validation

- **Final Output Creation**:
  - Complete result is generated according to task requirements
  - Output is formatted according to expected structure and schema
  - Result is validated against defined success criteria

- **Quality Assurance**:
  - Output is checked for completeness, accuracy, and consistency
  - Validation against known constraints and patterns
  - Uncertainty quantification for all predictions

- **Error Handling**:
  - If validation fails, error is logged and task is marked as failed
  - Root cause analysis is performed to identify failure origin
  - Automatic retry mechanism is triggered with exponential backoff

### 5. Task Completion and Reporting

- **Final Status Update**:
  - Task is marked as complete in the central task database
  - Final result is stored in the results repository
  - Task metadata is updated with completion time and status

- **Progress Reporting**:
  - Real-time progress visualization is updated
  - Task lifecycle is recorded from initiation to completion
  - Success rate and performance metrics are tracked

- **Feedback Loop**:
  - Task results are fed back into the system for learning
  - Performance data is used to optimize future task processing
  - Success patterns are identified for improved agent behavior

## Workflow Control Mechanisms

### 1. Task State Management

- Clear task state definitions:
  - Active: Task is being processed
  - Paused: Task has been temporarily halted
  - Failed: Task has encountered an error
  - Completed: Task has finished successfully
  - Retrying: Task is being attempted again

- State transitions with defined rules:
  - From Active to Failed with error detection
  - From Active to Paused with user intervention
  - From Failed to Retrying with retry policy
  - From Active to Completed with successful validation

### 2. Progress Monitoring

- Real-time progress tracking with defined milestones
- Progress percentage updated at key decision points
- Delay detection and alerting for significant slowdowns

### 3. Error Handling and Recovery

- Structured error handling with clear error codes
- Automatic retry with exponential backoff algorithm
- Failure root cause analysis with detailed logs
- Graceful degradation for partial failures

## Performance Optimization Strategies

### 1. Throughput Enhancement

- Dynamic workload balancing to prevent bottlenecks
- Predictive task allocation based on historical performance
- Adaptive batch processing to maximize throughput

### 2. Latency Reduction

- Task prioritization to minimize response time
- Message queue optimization to balance throughput and latency
- Caching of frequently accessed data and context

## Scalability Considerations

### 1. Horizontal Scaling

- Ability to add more agents to expand processing capacity
- Auto-scaling triggered by system load and workload patterns
- Load balancing distributed across available agents

### 2. Capacity Planning

- System capacity forecasting based on historical data
- Scalability limits defined for various workload scenarios
- Resource utilization thresholds to trigger scaling actions

## Reliability and Fault Tolerance

### 1. Failover Mechanisms

- Agent redundancy with automatic failover to backup agents
- Centralized task monitoring with real-time health checks
- Automatic retry for failed tasks with exponential backoff

### 2. System Recovery

- Transactional integrity to ensure consistent state after failures
- Atomic rollbacks to revert to stable state when processing fails
- State persistence with reliable storage mechanisms

## Security Considerations

### 1. Access Controls

- Granular access control for each agent and its capabilities
- Role-based access control with defined privilege levels
- Permission delegation with explicit access grants


## Context size and tooling infrastructure

Long-running agent workflows depend on maintaining and manipulating very
large chains of context.  As conversations grow past model token limits we
must plan for **context windowing, multipart rewriting, and skill discovery**.

**Motivation:**
Agents performing multi‑step workflows will accumulate interaction history that
cannot fit into a single prompt.  Without a strategy for fragmenting,
rewriting, and caching that history, downstream LLM calls either fail or lose
important state.  Additionally, tools and skills live under `.agents/skills`
and should be hot‑reloaded so agents can access new capabilities without
restart.

**Approaches:**

1. Adopt a shared `ContextManager` component (see roadmap design) that
   splits text into fixed‑size windows, tracks token counts, and supports
   rewriting earlier segments when new facts arrive.  Agents call the
   manager during the "Context Analysis" phase to obtain a compact
   summary.
2. Represent workflow state as a sequence of discrete context documents or
   "thoughts" stored separately; a coordinator composes the current working
   prompt from the most relevant documents plus the latest task input.  This
   facilitates partial recombination and pruning.
3. Create a lightweight service (possibly implemented in Rust for performance)
   that exposes an API for context operations and a watcher for the
   `.agents/skills` directory.  Agents make RPCs to obtain rewritten contexts
   and a list of available tools/skills.

**Success criteria:**

- Agents can handle conversations exceeding 1 million tokens without losing
  required information.
- New skill files added to `.agents/skills/` are discoverable by agents
  within 30 seconds of creation and usable in the next task.
- Unit tests simulate window boundary conditions and rewrite behaviour with
  100 % coverage.

**Dependencies:**

- Vector database or in‑memory index for context segments
- Conventions for skill metadata (YAML/JSON schema)
- Coordination between Python and Rust if a service is chosen

**Risks & Questions:**

- Rewriting must not discard still‑relevant facts; careful pinning or
  tagging of critical segments is necessary.
- Skill version mismatches could cause runtime errors; the registry may need
  checksums or migration support.


### Recursive Chain of Thought (CORT)

**Motivation:**
Agents often need to break complex problems into subproblems and reason
recursively.  The CORT pattern allows an agent to spawn child reasoning
paths, each maintaining its own context window.  This ties closely to the
workflow phases, especially "Context Analysis and Planning".

**Approaches:**

1. Implement a `ChainOfThought` object (see `src-old/classes/agent/*` for
   legacy inspiration) that records each reasoning step, forks when a
decision branches, and merges results once sub‑thoughts complete.  The
   object must be able to serialize to the context manager and rewind when
   backing out of a branch.
2. Use the existing task/strategy formulation phase to automatically insert
   CORT markers into the context so the LLM itself knows when to recurse.
3. Maintain separate context windows for each recursive depth and rely on a
   supervisor agent to orchestrate pushing/popping windows as the recursion
   unfolds.

**Success criteria:**

* Agents can recursively solve a multi‑step puzzle (e.g. planning a route,
  solving a math problem) with a depth of at least 5 without blowing token
  limits.
* The `ChainOfThought` data structure is covered by unit tests and used by
  two different agents (e.g. planner and verifier).
* Recursion tracing is visible in logs/debug UI to aid analysis.

**Dependencies:**

- Integration with the `ContextManager` to allocate windows per depth.
- Standards for serializing CORT nodes (likely JSON) under
  `.agents/skills` or a similar registry so tools can hook into them.
- Reference implementation or utilities from `src-old/classes/agent` such as
  `IncrementalProcessor` or `ParallelProcessor` which already handled
  subtask splitting.

**Risks & Questions:**

* Deep recursion could still exhaust resources; a depth limit and pruning
  policy are required.
* How should CORT results be cached or indexed for later reuse?



### 2. Communication Security

- End-to-end encryption for all inter-agent communication
- Secure channel establishment with certificate-based authentication
- Message integrity verification to prevent tampering

## Monitoring and Management

### 1. Performance Metrics

- System throughput measurements
- Average response time and latency
- Task processing duration
- Agent utilization rates

### 2. Operational Controls

- Real-time system health dashboard
- Alerting mechanisms for performance degradation and system failures
- Logging for all critical operations and errors

## Implementation Roadmap

Phase 1 (0-3 months): 
- Complete foundational design and specifications
- Develop prototype workflow and validation mechanisms

Phase 2 (3-6 months): 
- Implement core workflow phases with task processing
- Develop task state management and progress tracking
- Integrate error handling and recovery mechanisms

Phase 3 (6-12 months): 
- Add advanced workflow control capabilities
- Implement full fault tolerance and recovery mechanisms
- Optimize for high-performance throughput and low latency

This agent workflow design provides a comprehensive end-to-end processing sequence for agents within the PyAgent system, ensuring reliable, efficient, and secure task execution.

## Implementation Status

Core workflow components have already been prototyped and shipped:

* `src/core/workflow/task.py` now defines the `TaskState` enum and `Task` dataclass with a working `transition` method; unit tests exercise state names and transitions.
* `src/core/workflow/queue.py` implements `TaskQueue` around an `asyncio.Queue` and `tests/test_task_queue.py` verifies enqueue/dequeue behaviour.
* `src/core/workflow/engine.py` contains a minimal `WorkflowEngine` that processes one task and marks it COMPLETED; `tests/test_workflow_engine.py` confirms this behaviour.
* The `ContextManager` and `SkillsRegistry` libraries exist with associated tests (`tests/test_system_integration.py` and others), ensuring context windowing and dynamic skill discovery are functional.
* The recursive chain–of–thought (CORT) pattern is implemented in the `cort` package with unit tests (`tests/test_cort.py`) and integration coverage (`tests/integration/test_context_and_skills.py`).
* Supporting infrastructure such as the roadmap utilities, benchmarking modules, and governance helpers are live as described in their respective design documents.

These deliverables satisfy the initial success criteria for workflow phases, context handling, and recursive reasoning. Future implementation phases will expand on this foundation by enhancing error recovery, scaling, and advanced control mechanisms.