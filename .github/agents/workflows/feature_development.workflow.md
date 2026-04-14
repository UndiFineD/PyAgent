---
title: Feature Development Workflow
description: Develop and ship a new feature end-to-end
---

# Feature Development Workflow

**Description**: Develop and ship a new feature end-to-end

## Orchestration Steps

1. @10idea: Track and refine the initial feature idea.
2. @3design: Produce a technical design and sequence diagram.
3. @4plan: Break down the design into actionable sprint tasks via .github/agents/kanban/kanban.json.
4. @6code: Implement the feature codebase.
5. @5test: Write and execute unit tests for the code.
6. @8ql: Perform QA, static analysis, and CodeQL checks.
7. @9git: Stage, commit, and create a Pull Request.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
