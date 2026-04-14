---
agent: "4plan"
description: "Fallback rules and operational constraints for the 4plan agent."
---

# Base Rules: 4plan

These rules act as a resilient fallback for the `@4plan` agent. 
They may be dynamically updated by `@agentwriter`, 
or superseded by PostgreSQL database records during workflow orchestration.

## Core Constraints
1. **Preserve State**: Always log intermediate work to `.github/agents/data/`.
2. **Acknowledge Overrides**: 
    If the PostgreSQL schema provides a newer rule for a given context, 
    obey the database rule over this file.
3. **Continuous Learning**: 
    If a task fails, analyze the failure signature and propose updates 
    to this file via `@agentwriter` or using your own file editing tools.
4. **Scope Strictness**: 
    Do not perform tasks outside the explicit capabilities of `@4plan`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

- Preserved active hard-rule lessons: every task must include objective, target files, acceptance criteria, owner, and at least one deterministic validation command; conclusive gate evidence is required before DONE.

### Learned Rules & Historical Patterns

- Preserved active hard-rule lessons: every task must include objective, target files, acceptance criteria, owner, and at least one deterministic validation command; conclusive gate evidence is required before DONE.
