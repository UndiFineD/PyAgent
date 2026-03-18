# Architecture: System Context

This diagram provides a high-level overview of the PyAgent Fleet architecture, mapping the inter-dependencies between major system boundaries.

## System Context Diagram

```mermaid
C4Context
    title System Context diagram for PyAgent Fleet
    
    Person(dev, "Developer", "Lead Architect evolving the Swarm Intelligence.")
    Person(admin, "Administrator", "Manages deployments and fleet health.")
    
    Enterprise_Boundary(b0, "PyAgent Swarm") {
        System(core, "Core Logic", "Versioning, Dependency Resolving, BLAKE3 Hashing.")
        System(infra, "Infrastructure", "Fleet Manager, Sharding Orchestrator, Storage.")
        System(logic, "Logic Agents", "Cognitive, Development, and Security Agents.")
        System(obs, "Observability", "Structured Logging, Telemetry, and Metrics.")
    }
    
    System_Ext(llm, "LLM Providers", "GitHub Models, OpenAI, Ollama, VLLM.")
    System_Ext(github, "GitHub", "Version control and Pull Request management.")
    System_Ext(fs, "File System", "Local workspace where the agents operate.")
    
    Rel(dev, core, "Defines evolving patterns")
    Rel(dev, logic, "Instructs tasks via prompt.txt")
    Rel(admin, infra, "Monitors resource usage")
    
    Rel(core, infra, "Provides base classes & versions")
    Rel(infra, logic, "Orchestrates agent execution batches")
    Rel(logic, core, "Uses shared interfaces")
    Rel(logic, fs, "Reads/Writes project files")
    Rel(logic, llm, "Requests reasoning & code gen")
    Rel(infra, github, "Creates branches and PRs")
    Rel_D(logic, obs, "Emits events & telemetry")
    Rel_U(obs, core, "Provides self-healing feedback")
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Boundaries

| Boundary | Description | Key Modules |
|----------|-------------|-------------|
| **Core** | Fundamental logic, versioning, and workspace integrity. | `DependencyGraph`, `IncrementalProcessor`, `version.py` |
| **Infrastructure** | Fleet orchestration, sharding, and external resource management. | `AsyncFleetManager`, `ShardingOrchestrator`, `SecretManager` |
| **Logic** | The specialized agents performing the evolution tasks. | `CognitiveAgents`, `CoderAgent`, `SecurityAuditAgent` |
| **Observability** | Telemetry, logging, and metrics aggregation. | `StructuredLogger`, `OTelManager`, `GPUMonitor` |

---
*Generated automatically by `ArchitectureMapper.py` (Phase 236)*
