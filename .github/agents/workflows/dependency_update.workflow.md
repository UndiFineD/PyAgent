---
title: Dependency Maintenance Workflow
description: Update and test third-party dependencies
---

# Dependency Maintenance Workflow

**Description**: Update and test third-party dependencies

## Orchestration Steps

1. @dependabot: Review outdated dependencies and security alerts.
2. @dependencies: Bump version numbers in requirements.txt or package.json.
3. @e2e: Run end-to-end tests to verify nothing broke from the version bumps.
4. @gitops: Commit the dependency updates and trigger a CI pipeline.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
