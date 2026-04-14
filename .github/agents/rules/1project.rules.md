---
agent: "1project"
description: "Fallback rules and operational constraints for the 1project agent."
---

# Base Rules: 1project

These rules act as a resilient fallback for the `@1project` agent.
They may be dynamically updated by `@agentwriter`,
or superseded by PostgreSQL database records during workflow orchestration.

## Core Constraints

1. **Preserve State**:
    Always log intermediate work to `.github/agents/data/`.
2. **Acknowledge Overrides**:
    If the PostgreSQL schema provides a newer rule for a given context,
    obey the database rule over this file.
3. **Continuous Learning**:
    If a task fails, analyze the failure signature and propose updates
    to this file via `@agentwriter` or using your own file editing tools.
4. **Scope Strictness**:
    Do not perform tasks outside the explicit capabilities of `@1project`.
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules

- *(To be dynamically populated during runtime mapping and learning)*
