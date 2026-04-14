---
title: Codebase Refactoring Workflow
description: Clean and optimize legacy code
---

# Codebase Refactoring Workflow

**Description**: Clean and optimize legacy code

## Orchestration Steps

1. @profiling: Identify slow functions and performance bottlenecks.
2. @dead_code: Scan for and eliminate unused imports and obsolete functions.
3. @cleanup: Apply structural cleanup and linting rules (black, ruff, mypy).
4. @deduplication: Extract duplicated code blocks into shared utilities.
5. @testing: Validate the entire test suite against the refactored code.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
