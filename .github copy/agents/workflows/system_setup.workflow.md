---
title: New Environment Setup Workflow
description: Initialize a new project environment
---

# New Environment Setup Workflow

**Description**: Initialize a new project environment

## Orchestration Steps

1. @setup: Configure package managers, dependencies, and environment variables.
2. @filesystem: Pre-create standard operating directories (.github/agents/data, log, etc.).
3. @gitclone: Clone necessary external dependencies or submodule repositories.
4. @onboarding: Generate README.md and onboarding instructions for developers.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
